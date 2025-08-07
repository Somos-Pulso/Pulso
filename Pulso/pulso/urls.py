from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("accounts:login", permanent=False)),
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("department/", include('department.urls')),
    path("hospital/", include('hospital.urls')),
    path("notifications/", include('notification.urls')),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)