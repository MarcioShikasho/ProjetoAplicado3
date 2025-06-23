from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#a página só é acessada/carregada se o usuário estiver logado
@login_required 
def home(request):
    return render(request, 'home.html')  # Renderiza o template 'home.html'

