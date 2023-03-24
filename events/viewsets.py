from django.db.models import Prefetch

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from rowticket.decorators import query_debugger_detailed
from events.models import Category, Event, Ticket
from events.serializers import (
    CategorySerializer, CategoryBasicSerializer, EventDetailSerializer, EventListingSerializer
)


class CategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoryBasicSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(published=True, country=self.kwargs['country_country'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategorySerializer

        return super().get_serializer_class()


class EventViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.all()
    lookup_field = 'slug'
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(published=True, country=self.kwargs['country_country'])

        if self.action == 'retrieve':
            # Filter out unavailable tickets and prefetch tickets & sections
            queryset = queryset.prefetch_related(
                Prefetch(
                    'tickets',
                    queryset=Ticket.objects.with_availability().order_by('price').filter(available_quantity__gt=0)
                ),
                'tickets__section'
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListingSerializer

        return EventDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        highlighted_count = request.GET.get('highlighted', None)
        highlighted_events = None

        if highlighted_count and highlighted_count.isnumeric():
            highlighted_count = int(highlighted_count)

            if highlighted_count > 0:
                highlighted_events = queryset.filter(highlighted=True)[:highlighted_count]

                queryset = queryset.exclude(id__in=highlighted_events.values_list('id', flat=True))

        serializer = self.get_serializer(queryset, many=True)

        response = {
            'events': serializer.data
        }

        if highlighted_events is not None:
            response['highlighted_events'] = EventListingSerializer(highlighted_events, many=True, context={ 'request': self.request }).data

        return Response(response)
