from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from ..utils import time_execution
from pulso.logger import logger
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services import (ScheduleDetailService,
                        ScheduleListService,
                        PublishScheduleService,
                        CreateSheduleService,
                        ScheduleDeleteService)

class ScheduleDetailView(LoginRequiredMixin, View):
    template_name = 'hospital/schedule-detail.html'
    
    @time_execution
    def get(self, request, pk):
        try:
            
            user_id = request.user.id
            
            schedule_detail_service = ScheduleDetailService(
                schedule_id = pk,
                user_id = user_id
            )
            context = schedule_detail_service.schedule_data()
            
            return render(request, self.template_name, context)
        
        except ValueError as e:
            logger.error(f"Erro ao obter detalhes da escala: {str(e)}")
            return HttpResponseBadRequest(str(e))
        
        except Exception as e:
            logger.critical(f"Erro inesperado ao obter detalhes da escala: {str(e)}", exc_info=True)
            return HttpResponseServerError("Ocorreu um erro inesperado ao processar sua solicitação.")
        
class PublishScheduleView(LoginRequiredMixin, View):
    @time_execution
    def post(self, request, pk):
        try:
            user_id = request.user.id
            
            publish_schedule_service = PublishScheduleService(schedule_id=pk, user_id=user_id)
            publish_schedule_service.publish_schedule()
            
            messages.success(request, "Nova escala publicada com sucesso")
            return JsonResponse({"message": "Escala publicada com sucesso."})
        
        except PermissionError as e:
            logger.security(f"Erro de permissão ao publicar escala: {str(e)}")
            messages.error(request, str(e))
            return JsonResponse({"error": str(e)}, status=402)
        
        except ValueError as e:
            logger.error(f"Erro ao publicar escala: {str(e)}")
            messages.error(request, str(e))
            return JsonResponse({"error": str(e)}, status=400)
        
        except Exception as e:
            logger.critical(f"Erro inesperado ao publicar escala: {str(e)}", exc_info=True)
            messages.error(request, str(e))
            return HttpResponseServerError("Ocorreu um erro inesperado ao processar sua solicitação.")

class ScheduleListView(View):
    template_name = 'hospital/schedules-overview.html'

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        
        filters = {
            'period': request.GET.get('periodo'),
            'department_id': request.GET.get('departamento'),
            'status': request.GET.get('status'),
        }

        try:
            srv = ScheduleListService.get_instance()

            context = srv.get_user_schedules(user_id, filters)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string("hospital/escalas.html", context, request=request)
                return JsonResponse({'html': html})
        
            return render(request, self.template_name, context)
        
        except ValueError as e:
            logger.critical(f"Erro inesperado ao obter escalas: {str(e)}", exc_info=True)
            return HttpResponseBadRequest("Ocorreu um erro inesperado ao processar sua solicitação.")

class CreateScheduleView(View):
    template_name = 'hospital/schedule-create.html'

    def get(self, request):
        user_id = request.user.id
        departments = CreateSheduleService.get_departments_by_user_id(user_id)
        return render(request, self.template_name, {'departments': departments})

    def post(self, request):
        user_id = request.user.id
        departments = CreateSheduleService.get_departments_by_user_id(user_id)

        nome = request.POST.get('nome_escala', '').strip()
        start_date = request.POST.get('periodo_inicio')
        end_date = request.POST.get('periodo_fim')
        department_id = request.POST.get('setor_escala')

        error_message = None

        if not nome or not start_date or not end_date or not department_id:
            error_message = "Todos os campos são obrigatórios."
            return render(request, self.template_name, {'departments': departments, 'error_message': error_message})

        try:
            start_date_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Tenta criar a escala via service
            new_schedule = CreateSheduleService.create_schedule(nome, start_date_date, end_date_date, department_id)
            return redirect('hospital:schedule_detail', pk=new_schedule.pk)

        except ValueError:
            messages.error(request, "Formato de data inválido. Use o formato DD/MM/AAAA.")
            logger.error(f"Erro de formatação de data: {start_date} ou {end_date}")

        except ValidationError as ve:
            error = ve.messages[0].replace("YYYY-MM-DD", "DD/MM/AAAA") if ve.messages else "Erro de validação."
            messages.error(request, error)
            logger.error(f"Erro ao criar escala: {error}")

        except Exception as e:
            messages.error(request, "Erro inesperado ao criar escala.")
            logger.critical(f"Erro inesperado ao criar escala: {str(e)}", exc_info=True)

        return render(request, self.template_name, {'departments': departments})
    
class DeleteScheduleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        schedule_id = kwargs.get('pk')
        srv = ScheduleDeleteService.get_instance()

        try:
            srv.delete_schedule(schedule_id)
            success = True
            message = "Escala excluída com sucesso."

        except (ValidationError, ValueError) as e:
            success = False
            message = str(e)

        except Exception as e:
            success = False
            message = "Erro inesperado ao excluir escala."
            messages.error(request, f"{str(e)}")
            logger.critical(f"Erro inesperado ao deletar escala: {e}", exc_info=True)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "success": success,
                "message": message
            })

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return JsonResponse({
            "redirect_url": reverse("hospital:schedule_list"),
            "success": success,
            "message": message,
        })
