from rest_framework import serializers
from rest_framework.response import Response

from events.models import (
    Category, Event, EventImage, EventGalleryImage, Section, Ticket, Venue
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

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id','title')

class SectionSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = Section
        fields = ('id','name', 'color', 'event')


class TicketSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    available_quantity = serializers.SerializerMethodField()

    @staticmethod
    def get_available_quantity(ticket):
        return ticket.available_quantity

    class Meta:
        model = Ticket
        fields = (
            'identifier', 'section', 'cost', 'price', 'ticket_type', 'ready_to_ship', 'extra_info', 'quantity',
            'selling_condition', 'available_quantity', 'row','seller','status'
        )
class TicketCreateSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = Ticket
        fields = (
            'identifier', 'section', 'cost', 'price', 'ticket_type', 'ready_to_ship', 'extra_info', 'quantity',
            'selling_condition', 'row','seller','status'
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

    def get_starting_price(self, event):
        starting_price = getattr(event, 'starting_price', None)

        return starting_price

    def get_venue_name(self, event):
        return event.venue.name

    class Meta:
        model = Event
        fields = (
            'id','title', 'slug', 'date', 'date_text', 'venue_name', 'main_image_thumb',
            'starting_price', 'sections'
        )


class EventDetailSerializer(serializers.ModelSerializer):
    main_image_large = serializers.ImageField(read_only=True)
    event_images = EventImageSerializer(many=True)
    event_gallery_images = EventImageSerializer(many=True)
    tickets = TicketSerializer(many=True)
    venue = VenueSerializer()

    class Meta:
        model = Event
        fields = (
            'identifier', 'title', 'slug', 'date', 'date_text', 'venue',
            'main_image_large', 'event_images', 'event_gallery_images',
            'tickets'
        )
