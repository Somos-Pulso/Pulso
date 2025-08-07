from django.shortcuts import render
from django.views import View
from pulso.logger import logger
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services import (WelcomeService)

class WelcomeView(LoginRequiredMixin, View):
    template_name = 'accounts/welcome.html'
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        try:
            srv = WelcomeService.get_instance()

            context = srv.get_user_welcome(user_id)

            return render(request, self.template_name, context)

        except Exception as e:
            logger.critical(f"Erro inesperado ao publicar escala: {str(e)}", exc_info=True)
            return HttpResponseServerError("Ocorreu um erro inesperado ao processar sua solicitação.")