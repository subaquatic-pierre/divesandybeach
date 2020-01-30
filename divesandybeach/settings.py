"""
Django settings for divesandybeach project.

"""
import os
from .config import Config

config = Config()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Base Application definition settings
DEBUG = config.DEBUG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config.SECRET_KEY

SITE_ID = 1
WSGI_APPLICATION = 'divesandybeach.wsgi.application'
ROOT_URLCONF = 'divesandybeach.urls'
AUTH_USER_MODEL = 'core.User'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diving.apps.DivingConfig',
    'core.apps.CoreConfig',
    'django.contrib.sites',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_extensions',
    'tempus_dominus',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'diving.context_processors.nav_links',
            ],
        },
    },
]

# If debug is true then in development enviornment otherwise in production environment
if DEBUG == True:
    ALLOWED_HOSTS = []

    # TODO: Need to change to console once secure, remove host and user
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Production Environment
else:
    ALLOWED_HOSTS = ['divesandybeach', 'www.myriosdesign.com' 'myriosdesign.com',
                     '52.14.102.164', 'www.divesandybeach.com', 'divesandybeach.com']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # 'HOST': config.DB_HOST,
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            # 'USER': config.DB_USER,
            # 'PASSWORD': config.DB_PASSWORD,
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    ]

# All other settings

# Timezone settings
DATE_FORMAT = 'd m Y'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Django AllAuth settings
SOCIALACCOUNT_PROVIDERS = config.SOCIALACCOUNT_PROVIDERS
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Tempus Dominus Settings DateTimePicker
TEMPUS_DOMINUS_LOCALIZE = True
TEMPUS_DOMINUS_INCLUDE_ASSETS = False
