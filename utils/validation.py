from django.conf import settings

from rest_framework.exceptions import ValidationError

def validate_country(country):
    if not country or country not in settings.COUNTRY_LANGUAGES.keys():
        return Response({
            'country': 'Invalid country'
        }, status.HTTP_400_BAD_REQUEST)
