from rest_framework import mixins
from rest_framework import viewsets

from tncs.models import TnC
from tncs.serializers import TnCSerializer


class TnCViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TnC.objects.all()
    serializer_class = TnCSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(country=self.kwargs['country_country'])
