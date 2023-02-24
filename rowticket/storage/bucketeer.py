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
        """
        Normalizes the name so that paths like /path/to/ignored/../something.txt
        work. We check to make sure that the path pointed to is not outside
        the directory specified by the LOCATION setting.
        """
        try:
            return safe_join(self.location, (self.location + "/" + name))
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % f'{name} + {self.location}')