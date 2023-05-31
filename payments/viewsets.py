from rest_framework import mixins, viewsets

from payments.models import PaymentMethod
from payments.serializers import PaymentMethodSerializer


class PaymentMethodViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PaymentMethod.objects.all()
    lookup_field = 'identifier'
    pagination_class = None
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        queryset = super().get_queryset().specific()

        queryset = queryset.filter(active=True, country=self.kwargs['country_country'])

        return queryset
