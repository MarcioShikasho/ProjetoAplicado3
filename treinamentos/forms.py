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
    treinamento = forms.ModelChoiceField(queryset=Treinamento.objects.all(), label='Selecione o Treinamento')
    tipo_atribuicao = forms.ChoiceField(
        choices=[
            ('individual', 'Selecionar Colaboradores Individualmente'),
            ('cargo', 'Selecionar por Cargo')
        ],
        widget=forms.RadioSelect,
        initial='individual'
    )
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=Colaborador.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Selecione os Colaboradores'
    )
    cargo = forms.CharField(
        max_length=100,
        required=False,
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