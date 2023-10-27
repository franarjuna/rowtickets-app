from django.http import Http404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from mercadopago_payments.serializers import CreatePreferenceSerializer
from mercadopago_payments.models import MercadoPagoPaymentMethod, MercadoPagoPayment, MercadoPagoIPN
from orders.models import Order, ORDER_STATUSES

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

        mp = MercadoPagoPaymentMethod.objects.get()
        merchant_order = None
        if request.GET.get('topic') == 'merchant_order':
            merchant_order = request.GET.get('id')
        elif request.data.get('type') == 'payment':

            #merchant_order_get_preference = mp.get_preference(request.GET.get('data.id'))
            payment = mp.get_merchant_order_from_payment(request.data.get('data').get('id'))
            merchant_order = payment['order']['id']
            merchant_detail = mp.get_merchant(merchant_order)
            if(payment['status'] == 'approved' and payment['transaction_amount'] == payment['transaction_details']['total_paid_amount'] ):
                payment = get_object_or_404(MercadoPagoPayment, checkout_id=merchant_detail['response']['preference_id'])
                payment.order.status = ORDER_STATUSES['PAID']
                payment.order.payment_method = 'mercadopago'
                payment.order.payment_method_id = merchant_detail['response']['preference_id']
                payment.order.save()
            elif(payment['status'] == 'cancelled'):
                payment = get_object_or_404(MercadoPagoPayment, checkout_id=merchant_detail['response']['preference_id'])
                payment.order.status = ORDER_STATUSES['REJECTED']
                payment.order.payment_method = 'mercadopago'
                payment.order.payment_method_id = merchant_detail['response']['preference_id']
                payment.order.save()

        
        #merchant_detail = mp.get_merchant(merchant_order)
        #print(merchant_detail)
        #https://rowtickets-front.herokuapp.com/ar/compra-exitosa?collection_id=1314673418&collection_status=approved&payment_id=1314673418&status=approved&external_reference=4z642wcvps&payment_type=credit_card&merchant_order_id=11584231283&preference_id=58833378-e311ad07-13c3-41cb-9db0-82133e43658e&site_id=MLA&processing_mode=aggregator&merchant_account_id=null
        #merchant_order = '58833378-9a719a36-7d1d-4f42-bf14-b330b52ae44b'

        

        MercadoPagoIPN.objects.create(
            payment=payment,
            data=request.data
        )
        MercadoPagoIPN.objects.create(
            payment=payment,
            data=merchant_detail
        )


        return Response({})
