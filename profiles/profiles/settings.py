from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials
from decouple import config

# 1. Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Secret settings from .env
SECRET_KEY = config("DJANGO_SECRET_KEY", default="your-fallback-dev-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

# 3. Firebase setup
FIREBASE_CREDENTIALS = config("FIREBASE_CREDENTIALS")

# Optional check to debug issues
print("FIREBASE_CREDENTIALS:", FIREBASE_CREDENTIALS)
print("File exists?", os.path.exists(FIREBASE_CREDENTIALS))

if not firebase_admin._apps:
    if os.path.exists(FIREBASE_CREDENTIALS):
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    else:
        raise FileNotFoundError(f"Firebase credentials not found at: {FIREBASE_CREDENTIALS}")

# 4. Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",

    "profiles",  # your app
    "user",

    #'user.apps.UserConfig',   # custom user app

]

# 5. Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "profiles.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "profiles.wsgi.application"

# 6. Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 7. Authentication
AUTH_USER_MODEL = 'user.CustomUser'

# 8. Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 9. Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# 10. Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# 11. Default field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 12. Django REST Framework (optional customization)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "user.authentication.FirebaseAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'EXCEPTION_HANDLER': 'user.firebase_utils.custom_exception_handler',
    
}

# 13. CORS
CORS_ALLOW_ALL_ORIGINS = True  # consider setting this to False in production

# 14. Logging configuration
import logging.config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

                