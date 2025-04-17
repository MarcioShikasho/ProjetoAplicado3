from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from treinamentos.models import Treinamento
from contas.models import Conta


class Colaborador(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True) 
    cargo = models.CharField(max_length=100)
    matricula = models.IntegerField(unique=True, null=True, blank=True)
    data_admissao = models.DateField()

    usuario = models.OneToOneField(Conta, on_delete=models.CASCADE, related_name='colaborador', null=True, blank=True)

# Atribui o ID ao campo matricula e cria e-mail com o nome.matricula/id, depois que o objeto for salvo    
    def save(self, *args, **kwargs):
        criando = self.pk is None 

        super().save(*args, **kwargs)  # Primeiro save: cria o ID

        if criando and not self.matricula:
            self.matricula = self.id
            #super().save(update_fields=['matricula'])  # Segundo save: atribui o ID para matricula
    
        if criando and not self.usuario:
            self.criar_usuario()
            
        super().save(update_fields=['matricula', 'usuario', 'email'])  # Segundo save: gera o e-mail
        
    def criar_usuario(self):
        if self.id:
            email_usuario = f"{self.nome.lower()}.{self.id}@empresa.com"
            print(email_usuario)
            usuario = Conta.objects.create_user(
                email=email_usuario,
                password=self.cpf, 
                nome=self.nome
            )
        self.usuario = usuario    
            
    def __str__(self):
        return self.nome


class TreinamentoColaborador(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    treinamento = models.ForeignKey(Treinamento, on_delete=models.CASCADE)
    data_conclusao = models.DateField(null=True, blank=True)
    data_validade_treinamento = models.DateField(null=True, blank=True)

    def calcular_validade(self):
        if self.data_conclusao:
            prazo_validade = self.treinamento.prazo_validade  # Obtemos a validade do treinamento
            return self.data_conclusao + relativedelta(months=prazo_validade)
        return None 
    
    #Calcula a validade do treinamento a partir da data de conclusão
    def atualizar_validade_treinamento(self):
        if self.data_conclusao:
            data_final = self.data_conclusao + relativedelta(months=self.treinamento.prazo_validade)
            if data_final < timezone.now().date():
                self.data_validade_treinamento = None
            else:
                self.data_validade_treinamento = data_final
            self.save()
                    
    def __str__(self):
        return f"{self.colaborador.nome} - {self.treinamento.nome}"
