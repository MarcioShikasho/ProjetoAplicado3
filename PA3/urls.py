"""
URL configuration for PA3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView
from contas.views import CustomPasswordChangeView 
from contas.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('contas.urls')),
    path('colaboradores/', include('colaboradores.urls')),
    path('treinamentos/', include('treinamentos.urls')),
    path('', views.home, name='home'),
    path('redefinir-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('redefinir-senha/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('redefinir-senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('redefinir-senha/completo/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('alterar-senha/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('senha-alterada/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('contas/login/', CustomLoginView.as_view(), name='login'),
]
