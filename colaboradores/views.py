from django.shortcuts import render, redirect
from .models import Colaborador
from .forms import ColaboradorForm

def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/listar_colaboradores.html', {'colaboradores': colaboradores})

def criar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm()
    return render(request, 'colaboradores/criar_colaborador.html', {'form': form})

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

def excluir_colaborador(request, pk):
    colaborador = Colaborador.objects.get(pk=pk)
    colaborador.delete()
    return redirect('listar_colaboradores')
