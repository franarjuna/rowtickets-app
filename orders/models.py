from django.core.validators import MinValueValidator, MaxValueValidator
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
    (ORDER_STATUSES['IN_PROGRESS'], _('En proceso')),
    (ORDER_STATUSES['PENDING_PAYMENT_CONFIRMATION'], _('Esperando confirmación de pago')),
    (ORDER_STATUSES['PAID'], _('Paga')),
    (ORDER_STATUSES['CANCELLED'], _('Cancelada'))
)


class Order(CountrySpecificModel):
    user = models.ForeignKey(
        'users.User', verbose_name=_('comprador'), on_delete=models.PROTECT, related_name='orders'
    )
    status = models.CharField(_('estado'), max_length=50, choices=ORDER_STATUS_CHOICES)
    billing_address = models.OneToOneField(
        'addresses.Address', blank=True, null=True, verbose_name=_('Dirección de facturación'),
        on_delete=models.SET_NULL, related_name='order_billing_address'
    )
    shipping_address = models.OneToOneField(
        'addresses.Address', blank=True, null=True, verbose_name=_('Dirección de envío'),
        on_delete=models.SET_NULL, related_name='order_shipping_address'
    )
    per_ticket_service_charge = models.DecimalField(
        _('cargo de servicio por entrada'), max_digits=10, decimal_places=2
    )
    ticket_price_surcharge_percentage = models.DecimalField(
        _('porcentaje de recargo al precio base'), max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tickets_subtotal = models.DecimalField(_('subtotal de tickets'), max_digits=10, decimal_places=2)
    service_charge_subtotal = models.DecimalField(_('subtotal por cargo de servicio'), max_digits=10, decimal_places=2)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2)

    def __str__(self):
        return f'#{self.identifier}'

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
    price = models.DecimalField(_('precio final'), max_digits=10, decimal_places=2)
    cost = models.DecimalField(_('precio'), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    service_charge_subtotal = models.DecimalField(_('subtotal por cargo de servicio'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('ticket de compra')
        verbose_name_plural = _('tickets de compra')


class SellerTicket(OrderTicket):
    class Meta:
        proxy = True
        verbose_name = _('Liquidacion vendedor')
        verbose_name_plural = _('Liquidaciones vendedor')