from rest_framework import serializers

from countries.models import CountrySettings


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountrySettings
        fields = ('per_ticket_service_charge', 'ticket_price_surcharge_percentage')
