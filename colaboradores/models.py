from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from treinamentos.models import Treinamento
from contas.models import Conta
from django.utils.text import slugify
from unidecode import unidecode


class Colaborador(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField()
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(blank=True) 
    cargo = models.CharField(max_length=100)
    matricula = models.IntegerField(unique=True, null=True, blank=True)
    data_admissao = models.DateField()

    usuario = models.OneToOneField(Conta, on_delete=models.CASCADE, related_name='colaborador', null=True, blank=True)
    treinamentos = models.ManyToManyField(Treinamento, through='TreinamentoColaborador', related_name='colaboradores_inscritos', blank=True)
# Atribui o ID ao campo matricula e cria e-mail com o nome.matricula/id, depois que o objeto for salvo    
    def save(self, *args, **kwargs):           
        super().save(*args, **kwargs)  # Primeiro save: cria o ID
        self.refresh_from_db()
        
        atualizou_algo = False 
        verifica_pk = self.pk is None 

        if not verifica_pk:
            self.atualizar_email()
            
            if not self.matricula:
                self.matricula = self.id
                
                cargo_normalizado = unidecode(self.cargo.lower())
            
                if cargo_normalizado in ['tecnico', 'gerenciador']:
                    self.criar_usuario()
                
            atualizou_algo = True 

        if atualizou_algo:
            super().save(update_fields=['matricula', 'usuario', 'email'])                
            
    def criar_usuario(self):
        if self.id:
            nome_slug = slugify(self.nome)
            email_usuario = f"{nome_slug}.{self.matricula or self.id}@empresa.com"
            
            usuario = Conta.objects.create_user(
                email=email_usuario,
                password=self.cpf, 
                nome=self.nome
            )
        self.usuario = usuario
        self.email = email_usuario    
            
    def __str__(self):
        return self.nome

    def atualizar_email(self):
        if self.usuario:
            nome_slug = slugify(self.nome)
            novo_email = f"{nome_slug}.{self.matricula}@empresa.com"
            self.usuario.email = novo_email
            self.usuario.save()
            self.email = novo_email
            

class TreinamentoColaborador(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    treinamento = models.ForeignKey(Treinamento, on_delete=models.CASCADE)
    data_conclusao = models.DateField(null=True, blank=True)
    data_validade_treinamento = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('valido', 'Válido'),
        ('vencido', 'Vencido'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def calcular_validade(self):
        if self.data_conclusao:
            prazo_validade = self.treinamento.prazo_validade  # Pega o prazo de validade do treinamento
            return self.data_conclusao + relativedelta(months=prazo_validade)
        return None

    def atualizar_validade_treinamento(self):
        # Verifica se há data de conclusão
        if self.data_conclusao:
            # Calcula a data de validade
            data_final = self.data_conclusao + relativedelta(months=self.treinamento.prazo_validade)
            self.data_validade_treinamento = data_final

            # Atualiza o status dependendo da validade
            if data_final < timezone.now().date():
                self.status = 'vencido'  # Se a validade está no passado
            else:
                self.status = 'valido'  # Se a validade está no futuro
        else:
            # Se não há data de conclusão, o status é "pendente"
            self.status = 'pendente'

        # Salva o objeto para garantir que as mudanças sejam persistidas no banco de dados
        self.save()


    def __str__(self):
        return f"{self.colaborador.nome} - {self.treinamento.nome}"