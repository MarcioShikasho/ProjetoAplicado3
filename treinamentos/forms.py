from django import forms
from .models import Treinamento

class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = Treinamento
        fields = ['nome', 'descricao', 'prazo_validade', 'status']
