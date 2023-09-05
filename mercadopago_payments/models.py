from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

import mercadopago

from payments.models import PaymentMethod
from rowticket.models import AbstractBaseModel


class MercadoPagoPaymentMethod(PaymentMethod):
    access_token = models.CharField(_('Access token'), max_length=255, blank=False)
    public_key = models.CharField(_('Public key'), max_length=255, blank=False)

    payment_method = 'mercadopago'

    def create_preference(self, order, root_url):
        """
        Calls Mercado Pago gateway, creates the Payment Preference
        and returns the redirect url for the user.
        """
        sdk = mercadopago.SDK(self.access_token)

        order_items = [
            {
                'title': f'{order_ticket.ticket.event.title} - {order_ticket.ticket.section}',
                'quantity': order_ticket.quantity,
                'unit_price': float(order_ticket.ticket.price),
            } for order_ticket in order.order_tickets.all()
        ]

        order_items.append(
            {
                'title': 'Tasa general por servicio',
                'quantity': 1,
                'unit_price': float(order.service_charge_subtotal)
            }
        )

        preference_data = {
            'items': order_items,
            'external_reference': order.identifier,
            'back_urls': {
                'success': f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa'
            },
            'notification_url': f'{settings.BACKEND_BASE_URL}/countries/ar/mercadopago/ipn/',
            'binary_mode': True # Require instant payment confirmation
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response['response']


        MercadoPagoPayment.objects.create(
            request_data=preference_data,
            response_data=preference_response,
            order=order,
            payment_method=self,
            checkout_id=preference['id']
        )

        return preference['id']

    def get_merchant_order_from_payment(self, payment_id):
        sdk = mercadopago.SDK(self.access_token)

        payment = sdk.payment().get(payment_id)

        if payment['status'] == 404:
            return None

        print(payment)

        return payment['response']['order']['id']

    class Meta:
        verbose_name = _('Método de pago Mercado Pago')
        verbose_name_plural = _('Métodos de pago Mercado Pago')



class MercadoPagoPayment(AbstractBaseModel):
    order = models.ForeignKey(
        'orders.Order', related_name='MercadoPago_payments', verbose_name=_('compra'),
        blank=True, null=True, on_delete=models.PROTECT
    )
    payment_method = models.ForeignKey(
        MercadoPagoPaymentMethod, verbose_name=_('medio de pago'), on_delete=models.PROTECT,
        related_name='MercadoPago_payments'
    )

    request_data = models.JSONField(verbose_name=_('data (request)'))
    response_data = models.JSONField(verbose_name=_('data (response)'))
    checkout_id = models.CharField(_('checkout ID'), max_length=255, blank=True, unique=True, db_index=True)

    def __str__(self):
        return f'#{self.identifier}'

    class Meta:
        verbose_name = _('Pago MercadoPago')
        verbose_name_plural = _('Pagos MercadoPago')
        ordering = ('-created', )



class MercadoPagoIPN(AbstractBaseModel):
    payment = models.ForeignKey(
        MercadoPagoPayment, verbose_name=_('Pago MercadoPago'), on_delete=models.PROTECT,related_name='ipns'
    )

    data = models.JSONField(verbose_name=_('data (request)'))

    class Meta:
        verbose_name = _('IPN MercadoPago')
        verbose_name_plural = _('IPNs MercadoPago')
        ordering = ('-created', )