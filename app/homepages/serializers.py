from rest_framework import serializers

from events.serializers import EventBasicSerializer
from homepages.models import Homepage, HomepageSlide


class HomepageSlideSerializer(serializers.ModelSerializer):
    event = EventBasicSerializer(many=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = HomepageSlide
        fields = (
            'order', 'event', 'image_large'
        )


class HomepageDetailSerializer(serializers.ModelSerializer):
    slides = HomepageSlideSerializer(many=True)

    class Meta:
        model = Homepage
        fields = (
            'slides',
        )
