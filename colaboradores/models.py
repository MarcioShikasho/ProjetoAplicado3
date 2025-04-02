from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100)
    data_admissao = models.DateField()
    senha = models.CharField(max_length=12, default='senha123')
    
    def __str__(self):
        return self.nome
