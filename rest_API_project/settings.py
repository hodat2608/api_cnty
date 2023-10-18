
from pathlib import Path
from datetime import timedelta
import os
from allauth.account import app_settings
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-thz&h@j10k&9js=72yp6&v_^fdg6)l7y91uwg%kqal)&n@vh4x'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'NoteApp.apps.NoteappConfig',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'django_rest_passwordreset', 
    'accounts.apps.AccountsConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'rest_API_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'rest_API_project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_backend_session',
        'USER': 'root',
        'PASSWORD': '123456789',
        'PORT': 3306,
        'HOST': '127.0.0.1',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'build/static')]
STATIC_ROOT = os.path.join(BASE_DIR,'static') 


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'accounts.UserAccount'

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [ 
    #     'rest_framework.permissions.IsAuthenticated'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
]
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'accounts.backends.EmailBackend'
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_FROM = 'thieunao2o@gmail.com'
EMAIL_HOST_USER = 'thieunao2o@gmail.com'
EMAIL_HOST_PASSWORD = 'gwlx tctw gxbh ogld'
EMAIL_USE_TLS = True
SESSION_COOKIE_AGE = 86400
PASSWORD_RESET_TIMEOUT = 14400


CORS_ALLOWED_ORIGINS = [
    "http://localhost:2806",
    "http://localhost:3000",
]

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SOCIAL_AUTH_TOKEN_STRATEGY':'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['http://localhost:8000/google','http://localhost:8000/facebook'],
    'SERIALIZERS': {
        'user_create': 'accounts.serializers.UserCreateSerializer',
        'user': 'accounts.serializers.UserCreateSerializer',
        'current_user': 'accounts.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    }
}
USER_ID_FIELD = "id"
LOGIN_FIELD = "email"
PASSWORD_CHANGED_EMAIL_CONFIRMATION = True
LOGOUT_ON_PASSWORD_CHANGE = True
CREATE_SESSION_ON_LOGIN = True
SEND_ACTIVATION_EMAIL = True
USER_CREATE_PASSWORD_RETYPE = True,
SEND_CONFIRMATION_EMAIL = True
TOKEN_MODEL = "rest_framework.authtoken.models.Token"
PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND = True,
USERNAME_RESET_SHOW_EMAIL_NOT_FOUND = True,
PASSWORD_RESET_CONFIRM_URL ='password/reset/confirm/{uid}/{token}',
ACTIVATION_URL = 'activate/{uid}/{token}'
HIDE_USERS = True

from django.utils.module_loading import import_string
from django.apps import apps
from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject

class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super().__getattribute__(item)
        return val

EMAIL = ObjDict({
    "activation": "accounts.email_backends.ActivationEmail",
    "confirmation": "accounts.email_backends.ConfirmationEmail",
    "password_changed_confirmation": "accounts.email_backends.PasswordChangedConfirmationEmail",
    "password_reset": "accounts.email_backends.PasswordResetEmail",
    
})
SERIALIZERS = ObjDict({
    "activation": "accounts.serializers.ActivationSerializer",
    "resend_activation" : "accounts.serializers.SendEmailResetSerializer",
    "change_password": "accounts.serializers.ChangePasswordSerializer",
    "change_password_retype": "accounts.serializers.ChangePasswordRetypeSerializer",
    "token": "accounts.serializers.TokenSerializer",
    "token_create": "accounts.serializers.TokenCreateSerializer",
    "user": "accounts.serializers.UserSerializer",
    "password_reset": "accounts.serializers.SendEmailResetSerializer",
    "user_create": "accounts.serializers.UserCreateSerializer",
    "user_create_password_retype": "accounts.serializers.UserCreatePasswordRetypeSerializer",
    "current_user": "accounts.serializers.UserSerializer",
    "user_delete": "accounts.serializers.DeleteUserSerializer",
})

PERMISSIONS = ObjDict(
        {
            "activation": ["rest_framework.permissions.AllowAny"],
            "password_reset": ["rest_framework.permissions.AllowAny"],
            "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_password": ["accounts.permissions.CurrentUserOrAdmin"],
            "username_reset": ["rest_framework.permissions.AllowAny"],
            "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_username": ["accounts.permissions.CurrentUserOrAdmin"],
            "user_create": ["rest_framework.permissions.AllowAny"],
            "user_delete": ["accounts.permissions.CurrentUserOrAdmin"],
            "user": ["accounts.permissions.CurrentUserOrAdmin"],
            "user_list": ["accounts.permissions.CurrentUserOrAdmin"],
            "token_create": ["rest_framework.permissions.AllowAny"],
            "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
        }
    )

from accounts.constants import Messages as AccountMessages
CONSTANTS = {
    'messages': {
        'INVALID_CREDENTIALS_ERROR': AccountMessages.INVALID_CREDENTIALS_ERROR,
        'INACTIVE_ACCOUNT_ERROR': AccountMessages.INACTIVE_ACCOUNT_ERROR,
        'INVALID_TOKEN_ERROR': AccountMessages.INVALID_TOKEN_ERROR,
        'INVALID_UID_ERROR': AccountMessages.INVALID_UID_ERROR,
        'STALE_TOKEN_ERROR': AccountMessages.STALE_TOKEN_ERROR,
        'PASSWORD_MISMATCH_ERROR': AccountMessages.PASSWORD_MISMATCH_ERROR,
        'USERNAME_MISMATCH_ERROR': AccountMessages.USERNAME_MISMATCH_ERROR,
        'INVALID_PASSWORD_ERROR': AccountMessages.INVALID_PASSWORD_ERROR,
        'EMAIL_NOT_FOUND': AccountMessages.EMAIL_NOT_FOUND,
        'CANNOT_CREATE_USER_ERROR': AccountMessages.CANNOT_CREATE_USER_ERROR,
    }
}