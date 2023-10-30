from rest_framework import serializers
from rest_framework.response import Response

from events.models import (
    Category, Event, EventImage, EventGalleryImage, Section, Ticket, Venue, Organizer
)



class CategoryBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color')


class CategorySerializer(serializers.ModelSerializer):
    header_image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color', 'header_image_large')


class SectionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id','identifier','name', 'color', 'sub_section')
class EventSerializer(serializers.ModelSerializer):
    sections = SectionEventSerializer(many=True)
    class Meta:
        model = Event
        fields = ('id','identifier','title','formatted_date', 'date', 'sections')

class SectionSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = Section
        fields = ('id','identifier','name', 'color', 'event', 'sub_section', 'allow_row')

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ('id','identifier','name','slug','main_image','header_image','header_image')


class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    section = SectionSerializer()
    available_quantity = serializers.SerializerMethodField()

    @staticmethod
    def get_available_quantity(ticket):
        return ticket.available_quantity

    class Meta:
        model = Ticket
        fields = (
            'id','identifier', 'event', 'section', 'subsection', 'cost', 'price', 'ticket_type', 'ready_to_ship', 'extra_info', 'quantity',
            'selling_condition', 'available_quantity', 'row','seller','status', 'ready_date'
        )
class TicketCreateSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = Ticket
        fields = (
            'id','identifier', 'section', 'cost', 'price', 'ticket_type', 'ready_to_ship', 'extra_info', 'quantity',
            'selling_condition', 'row','seller','status', 'subsection'
        )


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('name', 'address')


class EventImageSerializer(serializers.ModelSerializer):
    image_large = serializers.ImageField(read_only=True)
    image_thumb = serializers.ImageField(read_only=True)

    class Meta:
        model = EventImage
        fields = (
            'order', 'image_large', 'image_thumb'
        )


class EventGalleryImageSerializer(serializers.ModelSerializer):
    image_large = serializers.ImageField(read_only=True)
    image_thumb = serializers.ImageField(read_only=True)

    class Meta:
        model = EventImage
        fields = (
            'order', 'image_large', 'image_thumb'
        )


class EventBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'date', 'date_text'
        )


class EventListingSerializer(serializers.ModelSerializer):
    main_image_thumb = serializers.ImageField(read_only=True)
    venue_name = serializers.SerializerMethodField()
    starting_price = serializers.SerializerMethodField()
    sections = SectionSerializer(many=True)
    organizer = OrganizerSerializer()

    def get_starting_price(self, event):
        starting_price = getattr(event, 'starting_price', None)

        return starting_price

    def get_venue_name(self, event):
        return event.venue.name

    class Meta:
        model = Event
        fields = (
            'id','identifier','title', 'slug', 'date', 'date_text', 'venue_name', 'main_image_thumb',
            'starting_price', 'sections', 'organizer','formatted_date'
        )

class EventHighSerializer(serializers.ModelSerializer):
    main_image_thumb = serializers.ImageField(read_only=True)
    venue_name = serializers.SerializerMethodField()
    starting_price = serializers.SerializerMethodField()
    organizer = OrganizerSerializer()

    def get_starting_price(self, event):
        starting_price = getattr(event, 'starting_price', None)

        return starting_price

    def get_venue_name(self, event):
        return event.venue.name

    class Meta:
        model = Event
        fields = (
            'id','identifier','title', 'slug', 'date', 'date_text', 'venue_name', 'main_image_thumb',
            'starting_price', 'organizer','formatted_date'
        )
class EventWithSectionsSerializer(serializers.ModelSerializer):
    main_image_thumb = serializers.ImageField(read_only=True)
    venue_name = serializers.SerializerMethodField()
    starting_price = serializers.SerializerMethodField()
    organizer = OrganizerSerializer()
    sections = SectionEventSerializer()

    def get_starting_price(self, event):
        starting_price = getattr(event, 'starting_price', None)

        return starting_price

    def get_venue_name(self, event):
        return event.venue.name

    class Meta:
        model = Event
        fields = (
            'id','identifier','title', 'slug', 'date', 'date_text', 'venue_name', 'main_image_thumb',
            'starting_price', 'organizer','formatted_date','sections'
        )


class EventDetailSerializer(serializers.ModelSerializer):
    main_image_large = serializers.ImageField(read_only=True)
    event_images = EventImageSerializer(many=True)
    event_gallery_images = EventImageSerializer(many=True)
    tickets = TicketSerializer(many=True)
    organizer = OrganizerSerializer()
    venue = VenueSerializer()

    class Meta:
        model = Event
        fields = (
            'id','identifier', 'title', 'slug', 'date', 'date_text', 'venue',
            'main_image_large', 'event_images', 'event_gallery_images',
            'tickets', 'organizer', 'individual_percentage'
        )
