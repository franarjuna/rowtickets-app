from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    #location = f'{settings.AWS_S3_ENDPOINT_URL}'
    location = 'public'
    default_acl = 'public-read'
    file_overwrite = False