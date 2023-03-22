from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.models import AbstractBaseModel, CountrySpecificModel


class Order(CountrySpecificModel):
    user = models.ForeignKey(
        'users.User', verbose_name=_('comprador'), on_delete=models.PROTECT, related_name='orders'
    )

    class Meta:
        verbose_name = _('compra')
        verbose_name_plural = _('compras')


class OrderTicket(AbstractBaseModel):
    order = models.ForeignKey(
        Order, verbose_name=_('compra'), on_delete=models.PROTECT, related_name='order_tickets'
    )
    ticket = models.ForeignKey(
        'events.ticket', verbose_name=_('ticket'), on_delete=models.PROTECT, related_name='order_tickets'
    )
    quantity = models.PositiveIntegerField(_('cantidad'))

    class Meta:
        verbose_name = _('ticket de compra')
        verbose_name_plural = _('tickets de compra')
