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
        timezone = 'America/Buenos_Aires'
        responseSuccessURL = f'{settings.FRONTEND_BASE_URL}/ar/compra-exitosa'
        responseFailURL = f'{settings.FRONTEND_BASE_URL}/ar/compra-fail'
        ipn = f'{settings.BACKEND_BASE_URL}/countries/ar/fiserv/ipn/'
        hash_algorithm = 'HMACSHA256'
        sharedsecret = self.api_key
        txndatetimetxt = txndatetime.strftime("%Y:%m:%d-%H:%M:%S")
        hashString = str(order.total) + "|" + currency + "|" + hash_algorithm + "|payonly|" + order.identifier + "|" + responseFailURL + "|" + responseSuccessURL + "|" + storename + "|" + timezone + "|" + ipn + "|" +  str(txndatetimetxt) + "|sale" 
        digest = hmac.new(sharedsecret.encode(), msg=hashString.encode(), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()

        response = {
             'url': url,
             'hashString': hashString,
             'ipg_args': [
                 {
                     'key':'txntype',
                     'value': 'sale'
                 },
                 {
                     'key':'txndatetime',
                     'value': txndatetimetxt
                 },
                 {
                     'key':'timezone',
                     'value': timezone
                 },
                 {
                     'key':'hash_algorithm',
                     'value': hash_algorithm
                 },
                 {
                     'key':'hashExtended',
                     'value': signature
                 },
                 {
                     'key':'storename',
                     'value': storename
                 },
                 {
                     'key':'mode',
                     'value': 'payonly'
                 },
                 {
                     'key':'responseSuccessURL',
                     'value': responseSuccessURL
                 },
                 {
                     'key':'responseFailURL',
                     'value': responseFailURL
                 },
                 {
                     'key':'transactionNotificationURL',
                     'value': ipn
                 },
                 {
                     'key':'oid',
                     'value': order.identifier
                 },
                 {
                     'key':'currency',
                     'value': currency
                 },
                 {
                     'key':'chargetotal',
                     'value': order.total
                 }
             ]
        }
        return response

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
