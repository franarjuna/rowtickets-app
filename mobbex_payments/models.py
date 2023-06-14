from decimal import Decimal
import json
import requests
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from countries.models import CountrySettings
from payments.models import PaymentMethod
from rowticket.models import AbstractBaseModel


class MobbexPaymentMethod(PaymentMethod):
    api_key = models.CharField(_('API Key'), max_length=255, blank=False)
    access_token = models.CharField(_('Access token'), max_length=255, blank=False)
    test_mode = models.BooleanField(_('modo test'))

    payment_method = 'mobbex'

    def create_checkout(self, order, root_url):
        url = 'https://api.mobbex.com/p/checkout'

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

        payload = {
            'total': float(order.total),
            'currency': 'ARS',
            'reference': order.identifier,
            'description': 'Compra en ROW Ticket',
            'items': order_items,
            'options': {
                'domain': urlparse(settings.FRONTEND_BASE_URL).netloc,
                'embed': True
            },
            'customer': {
                'email': order.user.email,
                'name': order.user.get_full_name(),
                'identification': '12345678'
            },
            'sources': ['visa', 'mastercard'],
            'test': self.test_mode,
            'return_url': f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa',
            'webhook': f'{settings.BACKEND_BASE_URL}/countries/ar/mobbex/ipn/'
        }

        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'x-access-token': self.access_token,
            'x-lang': 'es'
        }

        response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

        response_data = response.json()
        checkout_id = response_data['data']['id']

        MobbexPayment.objects.create(
            request_data=payload,
            response_data=response_data,
            order=order,
            payment_method=self,
            checkout_id=checkout_id
        )

        return checkout_id

    class Meta:
        verbose_name = _('Método de pago Mobbex')
        verbose_name_plural = _('Métodos de pago Mobbex')


class MobbexPayment(AbstractBaseModel):
    order = models.ForeignKey(
        'orders.Order', related_name='mobbex_payments', verbose_name=_('compra'),
        blank=True, null=True, on_delete=models.PROTECT
    )
    payment_method = models.ForeignKey(
        MobbexPaymentMethod, verbose_name=_('medio de pago'), on_delete=models.PROTECT,
        related_name='mobbex_payments'
    )

    request_data = models.JSONField(verbose_name=_('data (request)'))
    response_data = models.JSONField(verbose_name=_('data (response)'))
    checkout_id = models.CharField(_('checkout ID'), max_length=255, blank=True, unique=True, db_index=True)

    def __str__(self):
        return f'#{self.identifier}'

    class Meta:
        verbose_name = _('Pago Mobbex')
        verbose_name_plural = _('Pagos Mobbex')
        ordering = ('-created', )


class MobbexIPN(AbstractBaseModel):
    payment = models.ForeignKey(
        MobbexPayment, verbose_name=_('Pago Mobbex'), on_delete=models.PROTECT,related_name='ipns'
    )

    data = models.JSONField(verbose_name=_('data (request)'))

    class Meta:
        verbose_name = _('IPN Mobbex')
        verbose_name_plural = _('IPNs Mobbex')
        ordering = ('-created', )
