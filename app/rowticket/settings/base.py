from datetime import timedelta
import os
from pathlib import Path
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
SITE_NAME = 'ROW Ticket'

# Backend URL
API_BASE_URL = 'http://localhost:8000'

# Frontend URL & domain
FRONTEND_BASE_URL = 'http://localhost:3000'
DOMAIN = 'localhost:3000'

# Application definition
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'imagekit',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'adminsortable2',

    'events',
    'homepages',
    'rowticket',
    'users',

    'djoser' # Placed last so rowticket's templates override Djoser's
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'rowticket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'rowticket/templates'],
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

WSGI_APPLICATION = 'rowticket.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Enabled countries
COUNTRIES = (
    ('ar', _('Argentina')),
    ('cl', _('Chile'))
)

COUNTRY_LANGUAGES = {
    'ar': 'es-ar',
    'cl': 'es-cl'
}

# Internationalization
LANGUAGE_CODE = 'es-ar'

LANGUAGES = (
    ('es-ar', _('Español (Argentina)')),
    ('es-cl', _('Español (Chile)'))
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    }
]
AUTHENTICATION_BACKENDS = ['rowticket.authentication_backends.CaseInsensitiveEmailAuthenticationBackend']

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

COERCE_DECIMAL_TO_STRING = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATIC_URL = '/static/'
# Automatically versioned static file storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# TOKEN
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Easy Thumbnails
#  IMAGEKIT_CACHEFILE_DIR = 'thumbs'
#  IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'rowticket.imagekit_strategies.ImagekitOnSaveStrategy'

# SWAGGER
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# CORS - Cross-Origin Resource Sharing
CORS_ALLOW_HEADERS = list(default_headers) + [
    'contenttype',
]

# Celery
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True  # Prevent Celery from hiding exceptions when running on eager mode
CELERY_WORKER_HIJACK_ROOT_LOGGER = False  # Prevent Celery from capturing exceptions
CELERY_TIMEZONE = 'America/Argentina/Buenos_Aires'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_BACKEND = 'django-db'

# Jazzmin admin skin
JAZZMIN_SETTINGS = {
    'site_title': 'ROW Ticket Admin',
    'site_header': 'ROW Ticket',
    'site_brand': 'ROW Ticket',
    'custom_css': 'css/admin.css'
}

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'toolbar': [
                [
                    {'header': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                ],
                ['link'],
                ['clean'],
            ]
        }
    }
}
