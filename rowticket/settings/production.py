from __future__ import absolute_import, unicode_literals
import os
from pathlib import Path
import dj_database_url
from rowticket.settings.base import *
import django_heroku
import boto3

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ["SENTRY"],
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=0.1,
    send_default_pii=True,
)

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

if 'FRONTEND_BASE_URL' in os.environ:
    FRONTEND_BASE_URL = os.environ["FRONTEND_BASE_URL"]

if 'BACKEND_BASE_URL' in os.environ:
    BACKEND_BASE_URL = os.environ["BACKEND_BASE_URL"]

MAX_CONN_AGE = 600

ALLOWED_HOSTS = ["rowticket-app.herokuapp.com"]
DATABASES["default"] = dj_database_url.config(
    conn_max_age=MAX_CONN_AGE, ssl_require=True)

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://rowtickets-front.herokuapp.com',
    'http://localhost:3000'
]

MIDDLEWARE = MIDDLEWARE + [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite/static'),
]

AWS_ACCESS_KEY_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ['BUCKETEER_AWS_REGION']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
AWS_LOCATION = 'public/static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


DEFAULT_FILE_STORAGE = 'rowticket.storage.bucketeer.MediaStorage'  # <-- here is where we reference it

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
#EMAIL SMTP
if 'EMAIL_HOST' in os.environ:
    EMAIL_HOST = os.environ["EMAIL_HOST"]

if 'EMAIL_PORT' in os.environ:
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    
if 'EMAIL_HOST_USER' in os.environ:
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    
if 'EMAIL_HOST_PASSWORD' in os.environ:
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

if 'EMAIL_USE_SSL' in os.environ:
    EMAIL_USE_SSL = os.environ["EMAIL_USE_SSL"]

if 'EMAIL_USE_TLS' in os.environ:
    EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]

