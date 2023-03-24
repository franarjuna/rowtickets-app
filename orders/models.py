from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.models import AbstractBaseModel, CountrySpecificModel


ORDER_STATUSES = {
    'IN_PROGRESS': 'in_progress',
    'PENDING_PAYMENT_CONFIRMATION': 'pending_payment_confirmation',
    'PAID': 'paid',
    'CANCELLED': 'cancelled'
}


ORDER_STATUS_CHOICES = (
    ('in_progress', _('En proceso')),
    ('pending_payment_confirmation', _('Esperando confirmación de pago')),
    ('paid', _('Paga')),
    ('cancelled', _('Cancelada'))
)


class Order(CountrySpecificModel):
    user = models.ForeignKey(
        'users.User', verbose_name=_('comprador'), on_delete=models.PROTECT, related_name='orders'
    )
    status = models.CharField(_('estado'), max_length=50, choices=ORDER_STATUS_CHOICES)

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
