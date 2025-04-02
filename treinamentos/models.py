from django.db import models
from colaboradores.models import Colaborador

class Treinamento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    colaborador = models.ManyToManyField(Colaborador, related_name='treinamentos')

    def __str__(self):
        return self.nome
