"""
Django settings for divesandybeach project.

"""
import os
from .config import load_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = load_config(BASE_DIR)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Base Application definition settings
DEBUG = config.DEBUG
SECRET_KEY = config.SECRET_KEY

SITE_ID = 1
WSGI_APPLICATION = "divesandybeach.wsgi.application"
ROOT_URLCONF = "divesandybeach.urls"
AUTH_USER_MODEL = "core.User"

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(STATIC_ROOT, "core/")]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "diving.apps.DivingConfig",
    "core.apps.CoreConfig",
    "django.contrib.sites",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "django_extensions",
    "snowpenguin.django.recaptcha3",
    "tempus_dominus",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# If debug is true then in development enviornment otherwise in production environment
if DEBUG == True:
    ALLOWED_HOSTS = ["*"]

    RECAPTCHA_DISABLE = True

    # TODO: Need to change to console once secure, remove host and user
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    # Static files (CSS, JavaScript, Images)
    # MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")

# Production Environment
else:
    ALLOWED_HOSTS = ["3.15.1.157", "divesandybeach.com", "www.divesandybeach.com", "*"]
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            # 'HOST': config.DB_HOST,
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            # 'USER': config.DB_USER,
            # 'PASSWORD': config.DB_PASSWORD,
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Static files (CSS, JavaScript, Images)
    # MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")

# Django storages
STORAGES = {
    "default": {"BACKEND": "divesandybeach.storage.MediaStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = config.AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

# All other settings

# Timezone settings
DATE_FORMAT = "%d-%m-%Y"
DATE_INPUT_FORMAT = "%d-%m-%Y"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dubai"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Django AllAuth settings
SOCIALACCOUNT_PROVIDERS = config.SOCIALACCOUNT_PROVIDERS
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False

# Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

RECAPTCHA_PUBLIC_KEY = config.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = config.RECAPTCHA_PRIVATE_KEY
RECAPTCHA_DEFAULT_ACTION = "generic"
RECAPTCHA_SCORE_THRESHOLD = 0.5


# # Tempus Dominus Settings DateTimePicker
# TEMPUS_DOMINUS_LOCALIZE = True
# TEMPUS_DOMINUS_INCLUDE_ASSETS = False
