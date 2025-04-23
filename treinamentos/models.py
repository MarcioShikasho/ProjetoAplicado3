from django.db import models

class Treinamento(models.Model):
    STATUS_CHOICES = [
        ('naorealizado', 'Não Realizado'),
        ('emandamento', 'Em aplicação'),
        ('concluido', 'Concluído')
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='naorealizado')
    prazo_validade = models.IntegerField(help_text='Validade do treinamento em meses')
    
    colaboradores = models.ManyToManyField('colaboradores.Colaborador', through='colaboradores.TreinamentoColaborador', related_name='treinamentos_associados')
    
    def __str__(self):
        return self.nome