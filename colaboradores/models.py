from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from treinamentos.models import Treinamento
from contas.models import Conta
from django.utils.text import slugify
from unidecode import unidecode

CARGOS_COM_USUARIO = {'tecnico', 'gerencia', 'rh'}

class Colaborador(models.Model):
    CARGOS = [
        ('tecnico', 'Técnico'),
        ('gerencia', 'Gerência'),
        ('rh', 'RH'),
        
        ('assistente_administrativo', 'Assistente Administrativo'),
        ('analista_financeiro', 'Analista Financeiro'),
        ('contador', 'Contador'),
        ('analista_rh', 'Analista de RH'),

        ('tratorista', 'Tratorista'),
        ('operador_maquinas', 'Operador de Máquinas Agrícolas'),
        ('auxiliar_campo', 'Auxiliar de Campo'),
        ('encarregado_producao', 'Encarregado de Produção'),
        ('supervisor_agricola', 'Supervisor Agrícola'),

        ('engenheiro_agronomo', 'Engenheiro Agrônomo'),
        ('zootecnista', 'Zootecnista'),
        ('veterinario', 'Veterinário'),

        ('motorista', 'Motorista'),
        ('almoxarife', 'Almoxarife'),
        ('operador_armazem', 'Operador de Armazém'),
        ('supervisor_logistica', 'Supervisor de Logística'),

        ('representante_comercial', 'Representante Comercial'),
        ('consultor_tecnico_vendas', 'Consultor Técnico de Vendas'),
        ('coordenador_vendas', 'Coordenador de Vendas'),
        ('assistente_comercial', 'Assistente Comercial'),

        ('mecanico_agricola', 'Mecânico Agrícola'),
        ('eletricista', 'Eletricista'),
        ('encanador', 'Encanador'),
        ('supervisor_manutencao', 'Supervisor de Manutenção'),

        ('tecnico_suporte', 'Técnico de Suporte'),
        ('analista_sistemas', 'Analista de Sistemas'),
        ('desenvolvedor_software', 'Desenvolvedor de Software'),
    ]
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(blank=True, null=True, max_length=15)
    cargo = models.CharField(max_length=100, choices=CARGOS)
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
            
                if cargo_normalizado in CARGOS_COM_USUARIO:
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
                password = self.cpf.replace('.', '').replace('-', '') , 
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
    
    def is_tecnico(self):
        return self.cargo == 'tecnico'

    def is_gerencia(self):
        return self.cargo == 'gerencia'

    def is_rh(self):
        return self.cargo == 'rh'

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