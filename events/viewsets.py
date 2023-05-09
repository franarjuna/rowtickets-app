from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from events.models import Category, Event, Ticket, Section
from events.serializers import (
    CategorySerializer, CategoryBasicSerializer, EventDetailSerializer, EventListingSerializer, TicketSerializer
)
from users.models import User


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
        if self.action == 'list':
            queryset = Event.objects.with_starting_price()
        else:
            queryset = super().get_queryset()

        now = timezone.now()
        queryset = queryset.filter(published=True, country=self.kwargs['country_country'], date__gt=now)

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
            response['highlighted_events'] = EventListingSerializer(
                highlighted_events, many=True, context={ 'request': self.request }
            ).data

        return Response(response)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.with_availability().all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        event_ = Event.objects.filter(id=request.data.get('event_id')).first()
        section_ = Section.objects.filter(id=request.data.get('section_id')).first()
        seller = User.objects.filter(id=request.data.get('seller')).first()

        # Create a new ticket
        ticket = Ticket(
            event=event_,
            section=section_,
            row=request.data.get('row'),
            cost=request.data.get('cost'),
            price=request.data.get('price'),
            ticket_type=request.data.get('ticket_type'),
            selling_condition=request.data.get('selling_condition'),
            quantity=request.data.get('quantity'),
            ready_to_ship=request.data.get('ready_to_ship'),
            seller=seller
        )

        # Save the ticket to the database
        ticket.save()

        # Return a response
        return Response({'status': 'success'})
    
    def list(self, request, *args, **kwargs):
        my_tickets = TicketSerializer(Ticket.objects.with_availability().filter(seller=request.user), many=True).data
        return Response({'status': 'success','data': (my_tickets) })
