from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Senha alterada com sucesso. Faça login novamente.")
        logout(self.request)
        return response

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
