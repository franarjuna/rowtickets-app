from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join

class PublicMediaStorage(S3Boto3Storage):
    #location = f'{settings.AWS_S3_ENDPOINT_URL}'
    location = f'{settings.AWS_S3_ENDPOINT_URL}/public/'
    default_acl = 'public-read'
    file_overwrite = False
    
    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        # if not name.endswith('/'):
        #    name += "/"
        return safe_join(self.location, name)
        # name = self.location + name
        # return name