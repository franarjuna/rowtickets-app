from rest_framework import serializers

from rowticket.serializer_fields import IdentifierField


class CreateCheckoutSerializer(serializers.Serializer):
    order_identifier = IdentifierField(required=True)
    payment_method_identifier = IdentifierField(required=True)
