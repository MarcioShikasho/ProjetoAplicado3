from django.shortcuts import render, redirect
from .models import Treinamento
from .forms import TreinamentoForm

def listar_treinamentos(request):
    treinamentos = Treinamento.objects.all()
    return render(request, 'treinamentos/listar_treinamentos.html', {'treinamentos': treinamentos})

def criar_treinamento(request):
    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_treinamentos')
    else:
        form = TreinamentoForm()
    return render(request, 'treinamentos/criar_treinamento.html', {'form': form})

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
