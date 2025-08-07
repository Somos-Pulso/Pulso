from django.http import Http404, JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 


from notification.services import NotificationService
from notification.models import Notification


class NotificationListView(LoginRequiredMixin,View):
    """
    Displays all notifications received by the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        service = NotificationService.get_instance()
        notifications = service.get_user_notifications(request.user)

        # Passes the notifications to the template context
        return render(request, "notification/list.html", {
            "notifications": notifications
        })


class NotificationDetailView(LoginRequiredMixin, View):
    """
    Redirects the user to the target URL of the notification (if any),
    and marks the notification as read in the process.
    """

    def get(self, request, pk, *args, **kwargs):
        service = NotificationService.get_instance()

        notification = service.get_and_mark_as_read(pk, request.user.id)

        if notification is None:
            raise Http404("Notificação não encontrada.")

        target_url = service.get_url(notification)
        if target_url:
            return redirect(target_url)

        return render(request, "notification/detail.html", {
            "notification": notification
        })
    

class UnreadNotificationApiView(View):
    """
    Returns the last 10 unread notifications of the authenticated user in JSON.
    This view will be consumed by JS via the header dropdown.
    """

    def get(self, request, *args, **kwargs):
        service = NotificationService.get_instance()
        notifications = service.serialize_notifications(request.user, limit=10)

        return JsonResponse({
            "notifications": notifications
        })