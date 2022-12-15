from __future__ import absolute_import, unicode_literals

from rowticket.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

API_BASE_URL = 'http://localhost:8000'
FRONTEND_BASE_URL = 'http://localhost:3000'
DOMAIN = 'localhost:3000'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'devsecretkey'

ALLOWED_HOSTS = ['*']

try:
    from .local import *  # pylint: disable=wildcard-import
except ImportError:
    print('Please create a local.py settings file in your rowticket/settings/ folder, '
          + 'based on rowticket/settings/local.example.py')
    raise
