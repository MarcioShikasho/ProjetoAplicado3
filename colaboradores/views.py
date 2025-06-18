from django.shortcuts import render, redirect, get_object_or_404
from .models import Colaborador
from .forms import ColaboradorForm
from .forms import TreinamentoColaborador
from django.http import JsonResponse
from django.db.models import Q
from .permissoes import cargo_requerido

@cargo_requerido('rh', 'gerencia', 'tecnico')
def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/listar_colaboradores.html', {'colaboradores': colaboradores})

@cargo_requerido('rh', 'gerencia')
def cadastrar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm()
    return render(request, 'colaboradores/cadastrar.html', {'form': form})

@cargo_requerido('rh', 'gerencia')
def editar_colaborador(request, pk):
    colaborador = Colaborador.objects.get(pk=pk)
    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)
    return render(request, 'colaboradores/editar_colaborador.html', {'form': form})

@cargo_requerido('gerencia')
def excluir_colaborador(request, pk):
    colaborador = Colaborador.objects.get(pk=pk)
    colaborador.delete()
    return redirect('listar_colaboradores')

@cargo_requerido('rh', 'gerencia', 'tecnico')
def listar_treinamentos_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    treinamentos_relacionados = TreinamentoColaborador.objects.filter(colaborador=colaborador)

    return render(request, 'colaboradores/listar_treinamentos_colaborador.html', {
        'colaborador': colaborador,
        'treinamentos_relacionados': treinamentos_relacionados
    })
