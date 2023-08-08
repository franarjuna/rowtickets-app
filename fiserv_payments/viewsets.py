from decimal import Decimal

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, ORDER_STATUSES
from payments.serializers import CreateCheckoutSerializer
from fiserv_payments.models import FiservIPN, FiservPayment, FiservPaymentMethod


class FiservViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create_preference':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_checkout(self, request, *args, **kwargs):
        serializer = CreateCheckoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            order = request.user.orders.get(identifier=serializer.validated_data['order_identifier'])

            fiserv = FiservPaymentMethod.objects.get(
                country=self.kwargs['country_country'],
                identifier=serializer.validated_data['payment_method_identifier'],
                active=True
            )
            checkout_id = fiserv.create_checkout(order, '')

            return Response({ 'checkout_id': checkout_id })
        except (Order.DoesNotExist, FiservPaymentMethod.DoesNotExist):
            raise Http404

    @action(detail=False, methods=['post'])
    def ipn(self, request, *args, **kwargs):
        checkout_id = request.data['data']['checkout']['uid']

        payment = get_object_or_404(FiservPayment, checkout_id=checkout_id)

        FiservIPN.objects.create(
            payment=payment,
            data=request.data
        )

        if request.data['type'] == 'checkout':
            payment_data = request.data['data']['payment']

            if payment_data['status']['code'] == '200' and Decimal(payment_data['total']) == payment.order.total:
                # Payment status is OK and total matches order, mark order as paid
                payment.order.status = ORDER_STATUSES['PAID']
                payment.order.save()

        return Response({})