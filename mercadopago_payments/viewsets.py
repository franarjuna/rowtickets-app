from django.http import Http404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from mercadopago_payments.serializers import CreatePreferenceSerializer
from mercadopago_payments.models import MercadoPagoPaymentMethod, MercadoPagoPayment, MercadoPagoIPN


class MercadoPagoViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create_preference':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_preference(self, request, *args, **kwargs):
        serializer = CreatePreferenceSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            order = request.user.orders.get(identifier=serializer.validated_data['order_identifier'])

            mp = MercadoPagoPaymentMethod.objects.get(
                country=self.kwargs['country_country'],
                identifier=serializer.validated_data['payment_method_identifier'],
                active=True
            )
            preference_id = mp.create_preference(order, '')

            return Response({ 'preference_id': preference_id })
        except (Order.DoesNotExist, MercadoPagoPaymentMethod.DoesNotExist):
            raise Http404

    @action(detail=False, methods=['post'])
    def ipn(self, request, *args, **kwargs):
        print(request.data)
        print(kwargs)

        merchant_order = None

        if request.GET.get('topic') == 'merchant_order':
            merchant_order = request.GET.get('id')
        elif request.GET.get('type') == 'payment':
            mp = MercadoPagoPaymentMethod.objects.get()

            merchant_order = mp.get_merchant_order_from_payment(request.GET.get('data.id'))

        print(merchant_order)


        MercadoPagoIPN.objects.create(
            payment=payment,
            data=request.data
        )


        return Response({})
