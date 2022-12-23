from rest_framework import mixins, viewsets

from events.models import Event
from events.serializers import EventDetailSerializer


class EventViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Event.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(published=True)

    def get_serializer_class(self):
        return EventDetailSerializer
