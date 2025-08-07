import os
from pathlib import Path
from django.contrib.messages import constants as messages

# ==============================================================================
# CORE
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-9bcprecly15os*nzjys#%i3ytv%d&hf-pb1e&zkwv6ex$-7w1n"
DEBUG = True
ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_NAME = "pulso_session"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# APLICAÇÕES
# ==============================================================================

INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do projeto
    "accounts.apps.accountsConfig",
    "department.apps.departmentConfig",
    "hospital.apps.hospitalConfig",
    "notification.apps.notificationConfig",
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================================================================
# TEMPLATES
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "pulso", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# URLS / WSGI
# ==============================================================================

ROOT_URLCONF = "pulso.urls"
WSGI_APPLICATION = "pulso.wsgi.application"

# ==============================================================================
# BANCO DE DADOS
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pulso",
        "USER": "pulso",
        "PASSWORD": "pulso123@#",
        "HOST": "db",
        "PORT": "5432",
    }
}

# ==============================================================================
# AUTENTICAÇÃO
# ==============================================================================

AUTH_USER_MODEL = 'accounts.Professional'

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# MENSAGENS
# ==============================================================================

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ==============================================================================
# LOCALIZAÇÃO
# ==============================================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ==============================================================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ==============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "pulso", "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ==============================================================================
# SEGURANÇA
# ==============================================================================

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "https://0.0.0.0:8000",
]
