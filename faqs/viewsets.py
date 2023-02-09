from rest_framework import mixins
from rest_framework import viewsets

from faqs.models import FAQ
from faqs.serializers import FAQSerializer


class FAQViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(country=self.kwargs['country_country'])
