from decimal import Decimal
import json
import datetime
import locale
import requests
import hmac
import hashlib
import base64
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from countries.models import CountrySettings
from payments.models import PaymentMethod
from rowticket.models import AbstractBaseModel


class FiservPaymentMethod(PaymentMethod):
    api_key = models.CharField(_('Shared Secret'), max_length=255, blank=False)
    access_token = models.CharField(_('Store name'), max_length=255, blank=False)
    test_mode = models.BooleanField(_('modo test'))

    payment_method = 'fiserv'

    def create_checkout(self, order, root_url):
        response = dict()

        # PROD
        #url = "https://www5.ipg-online.com/connect/gateway/processing"
        url = "https://test.ipg-online.com/connect/gateway/processing"
        
        # DEV
        # response['url'] = "https://test.ipg-online.com/connect/gateway/processing"

        locale.setlocale(locale.LC_ALL, '')

        txndatetime = datetime.datetime.now()
        storename = self.access_token
        currency = '032'
        sharedsecret = self.api_key
        #txndatetimetxt = str(txndatetime.year) + ":" + str(txndatetime.month) + ":" + str(txndatetime.day) + "-" + str(txndatetime.hour) + ":" + str(txndatetime.minute) + ":" + str(txndatetime.second)
        txndatetimetxt = txndatetime.strftime("%Y:%m:%d-%H:%M:%S")
        hashString = storename + "|" +  str(txndatetimetxt) + "|" + str(order.total) + "|" + currency
        #hashs = binascii.hexlify(hashString.encode())
        digest = hmac.new(sharedsecret.encode(), msg=hashString.encode(), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()

        response = {
             'url': url,
             'ipg_args': {
                'txntype' : 'sale',
                'timezone' : "America/Buenos_Aires",
                'txndatetime' : txndatetimetxt,
                'hash_algorithm' : 'HMACSHA256',
                'hashExtended' : signature,
                'currency' : currency,
                'mode' : 'payonly',
                'storename' : storename,
                'chargetotal' : order.total,
                'language' : 'es_AR',
                'responseSuccessURL' : f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa',
                'responseFailURL' : f'{settings.FRONTEND_BASE_URL}/ar/compra-fail',
                'transactionNotificationURL' : f'{settings.BACKEND_BASE_URL}/countries/ar/fiserv/ipn/',
                'oid' : order.identifier,
             }
        }
        """
        response = {
             'url': url,
             'ipg_args': {
                'timezone' : "America/Buenos_Aires",
                'txndatetime' : txndatetimetxt,
                'hash_algorithm' : 'HMACSHA256',
                'hash' : hash.hexdigest(),
                'currency' : currency,
                'mode' : 'payonly',
                'storename' : storename,
                'chargetotal' : order.total,
                'language' : 'es_AR',
                'responseSuccessURL' : f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa',
                'responseFailURL' : f'{settings.FRONTEND_BASE_URL}/ar/compra-fail',
                'transactionNotificationURL' : f'{settings.BACKEND_BASE_URL}/countries/ar/fiserv/ipn/',
                'txntype' : 'sale',
                'checkoutoption' : 'classic',
                'dynamicMerchantName' : 'RowTicket Argentina',
                'authenticateTransaction' : 'true',
                'dccSkipOffer' : 'true',
                'oid' : order.identifier,
                'bname':'Name',
                'bcompany':'Name',
                'baddr1':'Name',
                'bcity':'Buenos Aires',
                'bstate':'B',
                'bcountry':'AR',
                'bzip':'1414',
                'phone':'123456789',
                'email':'test@test.com',
                'sname':'',
             }
        }
             """
        return response
        """
        $ipg_args['bname'] = $order->get_billing_first_name() . ' ' . $order->get_billing_last_name();
        $ipg_args['bcompany'] = $order->get_billing_company();
        $ipg_args['baddr1'] = $order->get_billing_address_1();
        $ipg_args['baddr2'] = $order->get_billing_address_2();
        $ipg_args['bcity'] = $order->get_billing_city();
        $ipg_args['bstate'] = $order->get_billing_state();
        $ipg_args['bcountry'] = $order->get_billing_country();
        $ipg_args['bzip'] = $order->get_billing_postcode();
        $ipg_args['phone'] = $order->get_billing_phone();
        $ipg_args['email'] = $order->get_billing_email();
        $ipg_args['fax'] = '';
        $ipg_args['sname'] = $order->get_shipping_first_name() . ' ' . $order->get_shipping_last_name();
        $ipg_args['saddr1'] = $order->get_shipping_address_1();
        $ipg_args['saddr2'] = $order->get_shipping_address_2();
        $ipg_args['scity'] = $order->get_shipping_city();
        $ipg_args['sstate'] = $order->get_shipping_state();
        $ipg_args['scountry'] = $order->get_shipping_country();
        $ipg_args['szip'] = $order->get_shipping_postcode();

        $token_id = wc_clean(WC()->session->get($this->id . '-token'));
        WC()->session->__unset($this->id . '-token');
        if ('yes' == $this->tokenisation && is_user_logged_in() == true) {
            if ($token_id != 'new' && !empty($token_id)) {
                $token = WC_Payment_Tokens::get($token_id);
                // Token user ID does not match the current user... bail out of payment processing.
                if ($token->get_user_id() !== wp_get_current_user()->ID) {
                    // Optionally display a notice with `wc_add_notice`
                    $this->log('malfunction ' . wp_get_current_user()->ID . ' user tried to access differnt user token ' . $token->get_user_id(), 'Error');
                    return;
                }
                if ($token) {
                    $ipg_args['hosteddataid'] = $token->get_token();
                    $ipg_args['hosteddatastoreid'] = $storename;
                }
            } else {
                $ipg_args['assignToken'] = 'true';
            }
        }


        return response
        "" "
        url = 'https://api.fiserv.com/p/checkout'

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
            'webhook': f'{settings.BACKEND_BASE_URL}/countries/ar/fiserv/ipn/'
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

        FiservPayment.objects.create(
            request_data=payload,
            response_data=response_data,
            order=order,
            payment_method=self,
            checkout_id=checkout_id
        )

        return checkout_id
        """

    class Meta:
        verbose_name = _('Método de pago Fiserv')
        verbose_name_plural = _('Métodos de pago Fiserv')


class FiservPayment(AbstractBaseModel):
    order = models.ForeignKey(
        'orders.Order', related_name='fiserv_payments', verbose_name=_('compra'),
        blank=True, null=True, on_delete=models.PROTECT
    )
    payment_method = models.ForeignKey(
        FiservPaymentMethod, verbose_name=_('medio de pago'), on_delete=models.PROTECT,
        related_name='fiserv_payments'
    )

    request_data = models.JSONField(verbose_name=_('data (request)'))
    response_data = models.JSONField(verbose_name=_('data (response)'))
    checkout_id = models.CharField(_('checkout ID'), max_length=255, blank=True, unique=True, db_index=True)

    def __str__(self):
        return f'#{self.identifier}'

    class Meta:
        verbose_name = _('Pago Fiserv')
        verbose_name_plural = _('Pagos Fiserv')
        ordering = ('-created', )


class FiservIPN(AbstractBaseModel):
    payment = models.ForeignKey(
        FiservPayment, verbose_name=_('Pago Fiserv'), on_delete=models.PROTECT,related_name='ipns'
    )

    data = models.JSONField(verbose_name=_('data (request)'))

    class Meta:
        verbose_name = _('IPN Fiserv')
        verbose_name_plural = _('IPNs Fiserv')
        ordering = ('-created', )
