from django.http import Http404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from mercadopago_payments.serializers import CreatePreferenceSerializer
from mercadopago_payments.models import MercadoPagoPaymentMethod


class MercadoPagoViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_preference(self, request):
        serializer = CreatePreferenceSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            order = request.user.orders.get(identifier=serializer.validated_data['order_identifier'])

            mp = MercadoPagoPaymentMethod.objects.get()
            preference_id = mp.create_preference(order, '')

            return Response({ 'preference_id': preference_id })
        except Order.DoesNotExist:
            raise Http404
