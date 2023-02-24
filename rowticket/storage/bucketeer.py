from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join

class PublicMediaStorage(S3Boto3Storage):
    location = f'{settings.AWS_S3_ENDPOINT_URL}/public'
    #location = 'public'
    enpoint_url = settings.AWS_S3_ENDPOINT_URL
    default_acl = 'public-read'
    file_overwrite = False
    
    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if not name.endswith('/'):
            name += "/"

        name += self.location
        return name