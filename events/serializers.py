from rest_framework import serializers

from events.models import Category, Event, EventImage, EventGalleryImage, EventPlaces, EventTickets


class CategoryBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color')


class CategorySerializer(serializers.ModelSerializer):
    header_image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'order', 'color', 'header_image_large')


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


class EventPlacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventPlaces
        fields = (
            'title', 'color'
        )


class EventTicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventTickets
        fields = (
            'place', 'title', 'price', 'ready_to_go', 'add_info', 'quantity', 'ticket_type', 'together'
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
    event_places = EventPlacesSerializer(many=True) 
    event_tickets = EventTicketsSerializer(many=True) 

    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'date', 'date_text', 'main_image_large',
            'event_images', 'event_gallery_images', 'event_tickets', 'event_places'
        )
