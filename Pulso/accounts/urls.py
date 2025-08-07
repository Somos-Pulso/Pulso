from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    WelcomeView,
    LoginView
    )

app_name = "accounts"

urlpatterns = [
    # sugestoes de possiveis urls

    path('', WelcomeView.as_view(), name='welcome'),

    # Autenticação
    
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='accounts:login'), name="logout"),

    # Conta do usuário (apenas o próprio)
    # path("profile/<int:pk>", None, name="profile_detail"),            
    # path("profile/edit/", None, name="profile_edit"),         
 
]