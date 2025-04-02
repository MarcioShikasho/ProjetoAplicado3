from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_treinamentos, name='listar_treinamentos'),
    path('criar/', views.criar_treinamento, name='criar_treinamento'),
    path('editar/<int:pk>/', views.editar_treinamento, name='editar_treinamento'),
    path('excluir/<int:pk>/', views.excluir_treinamento, name='excluir_treinamento'),
]
