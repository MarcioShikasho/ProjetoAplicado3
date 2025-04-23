from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django import forms
from django.contrib import messages
from .models import Treinamento
from .forms import TreinamentoForm, AtribuicaoTreinamentoForm
from colaboradores.models import Colaborador, TreinamentoColaborador


def listar_treinamentos(request):
    treinamentos = Treinamento.objects.all()
    return render(request, 'treinamentos/listar_treinamentos.html', {'treinamentos': treinamentos})


def cadastrar_treinamento(request):
    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_treinamentos')
    else:
        form = TreinamentoForm()
    return render(request, 'treinamentos/cadastrar_treinamento.html', {'form': form})


def editar_treinamento(request, pk):
    treinamento = Treinamento.objects.get(pk=pk)
    if request.method == "POST":
        form = TreinamentoForm(request.POST, instance=treinamento)
        if form.is_valid():
            form.save()
            return redirect('listar_treinamentos')
    else:
        form = TreinamentoForm(instance=treinamento)
    return render(request, 'treinamentos/editar_treinamento.html', {'form': form})


def excluir_treinamento(request, pk):
    treinamento = Treinamento.objects.get(pk=pk)
    treinamento.delete()
    return redirect('listar_treinamentos')


def atribuir_treinamento(request):
    if request.method == 'POST':
        form = AtribuicaoTreinamentoForm(request.POST)
        if form.is_valid():
            treinamento = form.cleaned_data['treinamento']
            tipo_atribuicao = form.cleaned_data['tipo_atribuicao']
            data_conclusao = form.cleaned_data.get('data_conclusao')
            
            # Determinar quais colaboradores receberão o treinamento
            if tipo_atribuicao == 'individual':
                colaboradores = form.cleaned_data.get('colaboradores', [])
                if not colaboradores:
                    form.add_error('colaboradores', 'Selecione pelo menos um colaborador.')
                    return render(request, 'treinamentos/atribuir_treinamento.html', {'form': form})
            elif tipo_atribuicao == 'cargo':
                cargo = form.cleaned_data.get('cargo', '')
                if cargo:
                    colaboradores = Colaborador.objects.filter(cargo=cargo)
                    if not colaboradores.exists():
                        form.add_error('cargo', 'Não há colaboradores com este cargo.')
                        return render(request, 'treinamentos/atribuir_treinamento.html', {'form': form})
                else:
                    form.add_error('cargo', 'Por favor, especifique um cargo.')
                    return render(request, 'treinamentos/atribuir_treinamento.html', {'form': form})
            
            # Atribuir o treinamento aos colaboradores selecionados
            contador = 0
            for colaborador in colaboradores:
                treinamento_colaborador, created = TreinamentoColaborador.objects.get_or_create(
                    colaborador=colaborador,
                    treinamento=treinamento
                )
                
                if data_conclusao:
                    treinamento_colaborador.data_conclusao = data_conclusao
                    treinamento_colaborador.atualizar_validade_treinamento()
                
                contador += 1
            
            # Mensagem de sucesso
            messages.success(request, f'Treinamento atribuído a {contador} colaboradores com sucesso!')
            return redirect('listar_treinamentos')
    else:
        form = AtribuicaoTreinamentoForm()
    
    return render(request, 'treinamentos/atribuir_treinamento.html', {'form': form})


def listar_colaboradores_treinamento(request, pk):
    treinamento = get_object_or_404(Treinamento, pk=pk)
    relacoes = TreinamentoColaborador.objects.filter(treinamento=treinamento)

    context = {
        'treinamento': treinamento,
        'relacoes': relacoes,
        'now': now(),
    }
    return render(request, 'treinamentos/listar_colaboradores_treinamento.html', context)


class RegistrarConclusaoForm(forms.ModelForm):
    class Meta:
        model = TreinamentoColaborador
        fields = ['data_conclusao']
        widgets = {
            'data_conclusao': forms.DateInput(format='%d/%m/%Y'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_conclusao'].input_formats = ['%d/%m/%Y']


def registrar_conclusao(request, pk):
    relacao = get_object_or_404(TreinamentoColaborador, pk=pk)
    
    if request.method == 'POST':
        form = RegistrarConclusaoForm(request.POST, instance=relacao)
        if form.is_valid():
            form.save()  # Salva a data de conclusão
            relacao.atualizar_validade_treinamento()  # Atualiza a validade e status
            return redirect('listar_colaboradores_treinamento', pk=relacao.treinamento.id)
    else:
        form = RegistrarConclusaoForm(instance=relacao)

    return render(request, 'treinamentos/registrar_conclusao.html', {
        'form': form,
        'relacao': relacao
    })

    
def remover_colaborador_treinamento(request, pk):
    relacao = get_object_or_404(TreinamentoColaborador, pk=pk)
    treinamento_id = relacao.treinamento.id
    relacao.delete()
    messages.success(request, 'Colaborador removido do treinamento com sucesso.')
    return redirect('listar_colaboradores_treinamento', pk=treinamento_id)