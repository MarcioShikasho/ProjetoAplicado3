from django import forms
from colaboradores.models import Colaborador
from .models import Treinamento


class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = Treinamento
        fields = ['nome', 
                  'descricao',
                  'prazo_validade',
                  'status',]

class AtribuicaoTreinamentoForm(forms.Form):
    treinamento = forms.ModelChoiceField(queryset=Treinamento.objects.all(), label='Treinamento')
    tipo_atribuicao = forms.ChoiceField(
        choices=[
            ('individual', 'Selecionar colaborador por ID'),
            ('cargo', 'Selecionar por cargo')
        ],
        widget=forms.RadioSelect,
        initial='individual'
    )
    colaborador_id = forms.CharField(
        required=False,
        label="Matrícula do Colaborador",
        widget=forms.TextInput(attrs={
            'list': 'colaboradores-list',
            'autocomplete': 'off',
            'placeholder': 'Digite a matrícula...',
            'class': 'form-control'
        })
    )
    cargo = forms.ChoiceField(
        choices=Colaborador.CARGOS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cargo'
    )
    data_conclusao = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datamask', 'type': 'text'}),
        label='Data de Conclusão (opcional)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_conclusao'].input_formats = ['%d/%m/%Y'] 