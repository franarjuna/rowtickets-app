from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response


class CountryViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(settings.COUNTRIES)
