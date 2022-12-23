from rest_framework import serializers

from events.models import Event


class EventDetailSerializer(serializers.ModelSerializer):
    main_image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'identifier', 'title', 'slug', 'date', 'date_text', 'main_image_large'
        )
