from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Category, Event
from events.serializers import CategoryBasicSerializer, EventListingSerializer
from homepages.models import Homepage
from homepages.serializers import HomepageDetailSerializer
from rowticket.decorators import query_debugger_detailed


class CountryViewSet(viewsets.ViewSet):
    lookup_field = 'country'

    def list(self, request):
        return Response(settings.COUNTRIES)

    @action(detail=True, methods=['get'])
    def homepage(self, request, country):
        request_context={ 'request': self.request }

        # Homepage data
        homepage = get_object_or_404(Homepage.objects.all(), country=country)
        homepage_data = HomepageDetailSerializer(homepage, context=request_context).data

        # Highlighted events data
        highlighted_events = Event.objects.filter(
            published=True, highlighted=True, country=country
        ).prefetch_related('venue')[:8]
        highlighted_events_data = EventListingSerializer(highlighted_events, many=True, context=request_context).data
        highlighted_event_ids = [highlighted_event.id for highlighted_event in highlighted_events]

        # Events per category
        categories = Category.objects.filter(published=True, country=country)
        category_data = CategoryBasicSerializer(categories, many=True).data

        i = 0

        for category in categories:
            category_data[i]['events'] = EventListingSerializer(Event.objects.filter(
                category=category, published=True
            ).exclude(
                id__in=highlighted_event_ids
            )[:8], many=True, context=request_context).data

            i += 1

        return Response({
            'homepage': homepage_data,
            'highlighted_events': highlighted_events_data,
            'categories': category_data
        })


    @action(detail=True, methods=['get'])
    def categories(self, request, country):
        request_context={ 'request': self.request }

        categories = Category.objects.filter(published=True, country=country)

        return Response(CategoryBasicSerializer(categories, many=True).data)
