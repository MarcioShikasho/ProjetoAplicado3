from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Criação do grupo de "Funcionários"
group, created = Group.objects.get_or_create(name='Gerenciadores')

#a página só é acessada/carregada se o usuário estiver logado
@login_required 
def home(request):
    return render(request, 'home.html')  # Renderiza o template 'home.html'

