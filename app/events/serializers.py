from rest_framework import serializers

from events.models import Event, EventImage, EventGalleryImage


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


class EventDetailSerializer(serializers.ModelSerializer):
    main_image_large = serializers.ImageField(read_only=True)
    event_images = EventImageSerializer(many=True)
    event_gallery_images = EventImageSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'date', 'date_text', 'main_image_large',
            'event_images', 'event_gallery_images'
        )
