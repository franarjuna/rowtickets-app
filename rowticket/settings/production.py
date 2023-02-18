from __future__ import absolute_import, unicode_literals
import os
from pathlib import Path

import dj_database_url

from rowticket.settings.base import *

DEBUG = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

MAX_CONN_AGE = 600

ALLOWED_HOSTS = ["rowticket-app.herokuapp.com"]
DATABASES["default"] = dj_database_url.config(
    conn_max_age=MAX_CONN_AGE, ssl_require=True)

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://rowticket-front.herokuapp.com/'
]

MIDDLEWARE = MIDDLEWARE + [
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
