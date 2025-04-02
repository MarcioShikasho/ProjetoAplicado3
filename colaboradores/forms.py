from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'sobrenome', 'email', 'cargo', 'data_admissao', 'senha']
