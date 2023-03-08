from django.conf import settings

def get_frontend_url(path_name, country):
    return '{}{}'.format(settings.FRONTEND_BASE_URL, settings.FRONTEND_URLS[path_name][country])
