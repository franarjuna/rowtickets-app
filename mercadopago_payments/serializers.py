from rest_framework import serializers

from rowticket.serializer_fields import IdentifierField


class CreatePreferenceSerializer(serializers.Serializer):
    order_identifier = IdentifierField(required=True)
    payment_method_identifier = IdentifierField(required=True)
    payment_installments = IdentifierField(required=False)
