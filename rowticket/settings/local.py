import dj_database_url
import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

IS_HEROKU = "DYNO" in os.environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]


MAX_CONN_AGE = 600

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd70l7ecjc521qp',
        'USER': 'cozanhbicwukpx',
        'PASSWORD': 'e1fb4734b5527d218170d292e936fcffad2dd2a1e2a782708fdf31468274300c',
        'HOST': 'ec2-34-194-73-236.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

# Generally avoid wildcards(*). However since Heroku router provides hostname validation it is ok
if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=MAX_CONN_AGE, ssl_require=True)
else:
    ALLOWED_HOSTS = []

# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU:
    DEBUG = True



# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]

if IS_HEROKU:
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATIC_URL = "static/"

    # Enable WhiteNoise's GZip compression of static assets.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    
    DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
    FTP_STORAGE_LOCATION = 'ftp://rowticket:?00ys3tG@claveglobal.com:21'
    BASE_URL = 'https://rowticket.claveglobal.com'
    