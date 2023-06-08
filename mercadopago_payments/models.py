from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

import mercadopago

from payments.models import PaymentMethod


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
                'unit_price': float(order.order_tickets.all()[0].quantity) * 100
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

        return preference['id']

    def get_merchant_order_from_payment(self, payment_id):
        sdk = mercadopago.SDK(self.access_token)

        payment = sdk.payment().get(payment_id)

        if payment['status'] == 404:
            return None

        print(payment)

        return payment['response']['order']['id']
