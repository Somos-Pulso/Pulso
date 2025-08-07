from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from pulso.logger import logger

class LoginView(DjangoLoginView):
    template_name = 'accounts/logins.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:welcome')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser:
            form.add_error(None, "Superusuários não podem acessar por aqui.")
            return self.form_invalid(form)
        
        # if not user.cpf:
        #     form.add_error(None, "Seu CPF não está preenchido. Contate o administrador.")
        #     return self.form_invalid(form)
        
        try:
            if not (user.is_doctor or user.is_manager):
                form.add_error(None, "Usuário sem permissão válida.")
                return self.form_invalid(form)
        except Exception:
            form.add_error(None, "Tipo de usuário desconhecido. Contate o administrador.")
            return self.form_invalid(form)

        return super().form_valid(form)