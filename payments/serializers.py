from rest_framework import serializers

from mercadopago_payments.models import MercadoPagoPaymentMethod
from payments.models import PaymentMethod
from rowticket.serializer_fields import IdentifierField


class CreateCheckoutSerializer(serializers.Serializer):
    order_identifier = IdentifierField(required=True)
    payment_method_identifier = IdentifierField(required=True)


class PaymentMethodSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if isinstance(instance, MercadoPagoPaymentMethod):
            ret['public_key'] = instance.public_key

        ret['payment_method'] = instance.payment_method

        return ret

    class Meta:
        model = PaymentMethod
        fields = ('identifier', 'display_name', 'created', 'modified')
