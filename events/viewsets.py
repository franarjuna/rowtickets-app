from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from events.models import Category, Event, Ticket, Section, Organizer
from events.serializers import (
    CategorySerializer, CategoryBasicSerializer, EventDetailSerializer, EventListingSerializer, EventSerializer, TicketSerializer,TicketCreateSerializer,SectionSerializer,OrganizerSerializer
)
from users.models import User
from datetime import datetime

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
                    queryset=Ticket.objects.with_availability().order_by('price').filter(available_quantity__gt=0, status=True)
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

        category_slug = request.GET.get('category', None)
        highlighted_count = request.GET.get('highlighted', None)
        highlighted_events = None

        if highlighted_count and highlighted_count.isnumeric():
            highlighted_count = int(highlighted_count)

            if highlighted_count > 0:
                highlighted_events = queryset.filter(highlighted=True)[:highlighted_count]

                # queryset = queryset.exclude(id__in=highlighted_events.values_list('id', flat=True))

        if category_slug != '':
            queryset = queryset.filter(category__slug=category_slug)

        serializer = self.get_serializer(queryset, many=True)

        response = {
            'events': serializer.data
        }

        if highlighted_events is not None:
            response['highlighted_events'] = EventListingSerializer(
                highlighted_events, many=True, context={ 'request': self.request }
            ).data

        return Response(response)


class TicketViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Ticket.objects.with_availability().all()
    serializer_class = TicketSerializer
    lookup_field = 'identifier'

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer

        return TicketSerializer

    def create(self, request, *args, **kwargs):

        
        self.request.data['seller'] = request.user.id
        self.request.data['event'] = EventSerializer(Event.objects.get(id=request.data.get('event_id'))).data
        self.request.data['section'] = SectionSerializer(Section.objects.get(id=request.data.get('section_id'))).data
        seller = User.objects.filter(id=request.user.id).first()

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        ticket = Ticket.objects.create(
            event=Event.objects.get(id=request.data.get('event_id')),
            section=Section.objects.get(id=request.data.get('section_id')),
            subsection=data.get('sub_section'),
            row=data.get('row'),
            cost=data.get('cost'),
            price=data.get('price'),
            ticket_type=data.get('ticket_type'),
            selling_condition=data.get('selling_condition'),
            quantity=data.get('quantity'),
            ready_to_ship=data.get('ready_to_ship'),
            ready_date=data.get('ready_date'),
            seller=seller,
        )

        serializer_create = TicketCreateSerializer(ticket)
        headers = self.get_success_headers(serializer_create.data)
        # Return a response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        now = datetime.now()
        my_tickets = TicketSerializer(Ticket.objects.with_availability().filter(seller=request.user, event__date__gte=now.date()), many=True).data
        return Response({'status': 'success','data': (my_tickets) })

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        return OrganizerSerializer    
    
    def list(self, request, *args, **kwargs):
        my_tickets = EventListingSerializer(Event.objects.filter(organizer=request.user), many=True).data
        return Response({'status': 'success','data': (my_tickets) })