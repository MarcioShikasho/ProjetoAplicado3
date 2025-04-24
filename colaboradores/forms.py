from django import forms
from .models import Colaborador, TreinamentoColaborador


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
        widgets = {
            'data_nascimento': forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datamask', 'type': 'text'}),
            'data_admissao': forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datamask', 'type': 'text'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nascimento'].input_formats = ['%d/%m/%Y']
        self.fields['data_admissao'].input_formats = ['%d/%m/%Y']       

        
class TreinamentoColaboradorForm(forms.ModelForm):
    class Meta:
        model = TreinamentoColaborador
        fields = ['colaborador', 'treinamento', 'data_conclusao']
        widgets = {
            'data_conclusao': forms.DateInput(attrs={'type': 'date'}),
        }