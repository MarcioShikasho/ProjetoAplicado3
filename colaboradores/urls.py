from django.urls import path
from . import views

urlpatterns = [
    path('listar_colaboradores', views.listar_colaboradores, name='listar_colaboradores'),
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('editar/<int:pk>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir/<int:pk>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('treinamentos/<int:colaborador_id>/', views.listar_treinamentos_colaborador, name='listar_treinamentos_colaborador'),
]
