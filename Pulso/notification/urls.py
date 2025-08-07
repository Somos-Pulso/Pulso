from django.urls import path

from notification.views import NotificationListView, NotificationDetailView, UnreadNotificationApiView



app_name = "notification"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("<int:pk>/", NotificationDetailView.as_view(), name="detail"),
    path("api/unread/", UnreadNotificationApiView.as_view(), name="unread_api"),
]