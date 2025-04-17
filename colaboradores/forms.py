from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome',
                  'sobrenome',
                  'cpf',
                  'data_nascimento', 
                  'telefone',
                  'cargo', 
                  'data_admissao',]
