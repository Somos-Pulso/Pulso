from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ValidationError
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from ..utils import time_execution
from pulso.logger import logger
from ..services import (CreateShiftServices,
                        DeleteShiftServices,
                        UpdateShiftServices,
                        ShiftViewService,
                        ShiftListService)

class ListShiftView(LoginRequiredMixin, View):
    @time_execution
    def get(self, request):
        user_id = request.user.id
        dept_filter = request.GET.get('departamento', 'everything')
        
        service = ShiftListService()

        context = service.get_user_shifts(
            user_id=user_id,
            dept=dept_filter
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'hospital/shifts-list.html', context)
            
        return render(request, 'hospital/shifts-overview.html', context)

class DetailShift(LoginRequiredMixin, View):
    
    @time_execution
    def get(self, request, pk):
        user_id = request.user.id
        shift_id = pk

        service = ShiftViewService()
        context = service.get_shift(shift_id = shift_id)

        return render(request, 'hospital/shift-detail.html', context)
    
class CreateShiftView(LoginRequiredMixin, View):
    
    @time_execution
    def post(self, request):
        try:
            body = json.loads(request.body)

            user_id = request.user.id
            schedule_id = body['schedule_id']
            shift_data = body['shift']

            create_shift_service = CreateShiftServices(
                schedule_id=schedule_id,
                shift_data=shift_data,
                user_id=user_id
            )
            create_shift_service.create_shift()
            shift = create_shift_service.new_shift()
            return JsonResponse({
                    "shift": {
                        "id": shift.get("id"),
                        "date": shift.get("date"),
                        "start_time": shift.get("start_time"),
                        "end_time": shift.get("end_time"),
                        "description": shift.get("description", ""),
                        "type": shift.get("type"),
                        "allocations": shift.get("allocations", [])
                    }
                }, status=201)

        except PermissionError as e:
            logger.security(f"Erro de permissão ao criar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=403)

        except ValueError or ValidationError as e:
            logger.error(f"Erro ao criar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=404)

        except Exception as e:
            logger.critical(f"Erro inesperado ao criar plantão: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Erro interno ao criar plantão."}, status=500)
        
class DeleteShiftView(LoginRequiredMixin, View):
    @time_execution
    def delete(self, request, pk):
        try:
            user_id = request.user.id

            delete_shift = DeleteShiftServices(shift_id=pk, user_id=user_id)
            delete_shift.delete_shift()
            return HttpResponse(status=204)

        except PermissionError as e:
            logger.security(f"Erro de permissão ao deletar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=403)

        except ValueError or ValidationError as e:
            logger.error(f"Erro ao deletar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=404)

        except Exception as e:
            logger.critical(f"Erro inesperado ao deletar plantão: {str(e)}", exc_info=True)
            return JsonResponse({"error": f"Erro interno ao deletar plantão.{str(e)}"}, status=500)
        
class UpdateShiftView(LoginRequiredMixin, View):
    @time_execution
    def put(self, request, pk):
        try:
            body = json.loads(request.body)

            user_id = request.user.id
            shift_data = body['shift']

            update_services = UpdateShiftServices(
                shift_id=pk,
                shift_data=shift_data,
                user_id=user_id
            )
            update_services.update_shift()
            shift = update_services.updated_shift()
            return JsonResponse({
                "shift": {
                    "id": shift.get("id"),
                    "date": shift.get("date"),
                    "start_time": shift.get("start_time"),
                    "end_time": shift.get("end_time"),
                    "description": shift.get("description", ""),
                    "type": shift.get("type"),
                    "allocations": shift.get("allocations", [])
                }
            }, status=200)

        except PermissionError as e:
            logger.security(f"Erro de permissão ao atualizar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=403)

        except ValueError or ValidationError as e:
            logger.error(f"Erro ao atualizar plantão: {str(e)}")
            return JsonResponse({"error": str(e)}, status=404)

        except Exception as e:
            logger.critical(f"Erro inesperado ao atualizar plantão: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Erro interno ao atualizar plantão."}, status=500)
