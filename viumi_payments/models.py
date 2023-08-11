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


class ViumiPaymentMethod(PaymentMethod):
    api_key = models.CharField(_('ID Cliente'), max_length=255, blank=False)
    access_token = models.CharField(_('Client Secret'), max_length=255, blank=False)
    test_mode = models.BooleanField(_('modo test'))

    payment_method = 'viumi'

    def create_checkout(self, order, root_url):

        json_data = {
            "grant_type": "client_credentials",
            "client_id": self.access_token,
            "client_secret": self.api_key,
            "scope": "*"
        }

        response_token = requests.post('https://auth.geopagos.com/oauth/token', json=json_data)
        response_token_data = response_token.json()
        print(response_token_data)

        url = 'https://api.viumi.com.ar/api/v2/orders'

        order_items = [
            {
                'id': 1,
                'name': f'{order_ticket.ticket.event.title} - {order_ticket.ticket.section}',
                'quantity': order_ticket.quantity,
                'unitPrice': {
                    'currency': '032',
                    'amount': float(order_ticket.ticket.price)*100
                },
            } for order_ticket in order.order_tickets.all()
        ]

        order_items.append(
            {
                'id':2,
                'name': 'Tasa general por servicio',
                'quantity': 1,
                'unitPrice': {
                    'currency': '032',
                    'amount': float(order.service_charge_subtotal)*100
                }
            }
        )
        external_data = ''
        payload = {
            'data': {
                'attributes': {
                    'items': order_items,
                    "redirect_urls": {
                        "success": f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa',
                        "failed": f'{settings.FRONTEND_BASE_URL}/ar/compra-fail',
                    },
                    'externalData': external_data
                }
            }
        }
        """
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
            'webhook': f'{settings.BACKEND_BASE_URL}/countries/ar/viumi/ipn/'
        }
"""
        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'Authorization': 'Bearer ' + response_token_data['access_token']
        }

        response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

        response_data = response.json()

        ViumiPayment.objects.create(
            request_data=payload,
            response_data=response_data,
            order=order,
            payment_method=self,
            checkout_id=response_data
        )

        return response_data

    class Meta:
        verbose_name = _('Método de pago Viumi')
        verbose_name_plural = _('Métodos de pago Viumi')


class ViumiPayment(AbstractBaseModel):
    order = models.ForeignKey(
        'orders.Order', related_name='viumi_payments', verbose_name=_('compra'),
        blank=True, null=True, on_delete=models.PROTECT
    )
    payment_method = models.ForeignKey(
        ViumiPaymentMethod, verbose_name=_('medio de pago'), on_delete=models.PROTECT,
        related_name='viumi_payments'
    )

    request_data = models.JSONField(verbose_name=_('data (request)'))
    response_data = models.JSONField(verbose_name=_('data (response)'))
    checkout_id = models.CharField(_('checkout ID'), max_length=255, blank=True, unique=True, db_index=True)

    def __str__(self):
        return f'#{self.identifier}'

    class Meta:
        verbose_name = _('Pago Viumi')
        verbose_name_plural = _('Pagos Viumi')
        ordering = ('-created', )


class ViumiIPN(AbstractBaseModel):
    payment = models.ForeignKey(
        ViumiPayment, verbose_name=_('Pago Viumi'), on_delete=models.PROTECT,related_name='ipns'
    )

    data = models.JSONField(verbose_name=_('data (request)'))

    class Meta:
        verbose_name = _('IPN Viumi')
        verbose_name_plural = _('IPNs Viumi')
        ordering = ('-created', )
