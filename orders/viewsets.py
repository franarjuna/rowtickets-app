from django.db.models import Prefetch, Q

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from rowticket.decorators import query_debugger_detailed
from events.models import Category, Event, Ticket
from orders.models import Order


class OrderViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    lookup_field = 'slug'
    pagination_class = None
    
    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(country=self.kwargs['country_country'])