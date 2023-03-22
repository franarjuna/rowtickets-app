from rest_framework import serializers

from events.models import Category, Event, EventImage, EventGalleryImage, Section, Ticket


class CategoryBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color')


class CategorySerializer(serializers.ModelSerializer):
    header_image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color', 'header_image_large')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('name', 'color')


class TicketSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = Ticket
        fields = (
            'identifier', 'section', 'price', 'ticket_type', 'ready_to_ship', 'extra_info', 'quantity',
            'selling_condition'
        )


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

    def get_venue_name(self, event):
        return event.venue.name

    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'date', 'date_text', 'venue_name', 'main_image_thumb'
        )


class EventDetailSerializer(serializers.ModelSerializer):
    main_image_large = serializers.ImageField(read_only=True)
    event_images = EventImageSerializer(many=True)
    event_gallery_images = EventImageSerializer(many=True)
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'date', 'date_text', 'main_image_large',
            'event_images', 'event_gallery_images', 'tickets'
        )
