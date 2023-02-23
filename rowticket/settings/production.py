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

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0.1,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

DEBUG = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


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

AWS_ACCESS_KEY_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ['BUCKETEER_AWS_REGION']
AWS_DEFAULT_ACL = None
# AWS_S3_SIGNATURE_VERSION = os.environ['S3_SIGNATURE_VERSION', 's3v4']
AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
PUBLIC_MEDIA_LOCATION = 'public'

MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
#DEFAULT_FILE_STORAGE = 'rowticket.backends.bucketeer.PublicMediaStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PRIVATE_MEDIA_DEFAULT_ACL = 'private'
PRIVATE_MEDIA_LOCATION = 'media/private'
# PRIVATE_FILE_STORAGE = 'example.utils.storage_backends.PrivateMediaStorage'


django_heroku.settings(locals())