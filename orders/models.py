from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.models import AbstractBaseModel, CountrySpecificModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from countries.utils import get_country_from_language_code
from emails.tasks import send_mail
from rowticket.fields import LanguageCodeField
from rowticket.frontend_urls import get_frontend_url
from events.models import Ticket, Event, Section
from users.models import User

from django.conf import settings

ORDER_STATUSES = settings.ORDER_STATUSES
ORDER_STATUS_CHOICES = settings.ORDER_STATUS_CHOICES



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


    
    def save_model(self, request, obj, form, change):
        update_fields = []
        for key, value in form.cleaned_data.items():
            # True if something changed in model
            if value != form.initial[key]:
                update_fields.append(key)

        obj.save(update_fields=update_fields)


    class Meta:
        verbose_name = _('compra')
        verbose_name_plural = _('compras')

@receiver(post_save, sender= Order)
def send_tracking_email(sender, instance, created, update_fields, **kwargs):
    if created == False and 'status' in update_fields:
        #tickets 
        order_tickets = OrderTicket.objects.get(order = instance.id)
        ticket = Ticket.objects.get(id = order_tickets.ticket_id)
        section = Section.objects.get(id = ticket.section_id) 
        event = Event.objects.get(id = ticket.event_id) 
        seller = User.objects.get(id = ticket.seller_id) 
        buyer = User.objects.get(id = instance.user_id) 
        
        product_name = str(event.title) + ' ' + event.date.strftime('%x %X')

        product_detail = _('Sector') + ": " + str(section.name) 
        if ticket.subsection!= None:
            product_detail = product_detail + ' - ' + str(ticket.subsection)
        
        if ticket.row!= None:
            product_detail = product_detail + ' ' + _('Fila') + ": " + str(ticket.row)

        details = {
                'product_name': product_name,
                'product_detail': product_detail,
                'product_quant': order_tickets.quantity,
                'product_price': order_tickets.cost,
                'product_price_total': order_tickets.quantity * order_tickets.cost,
                'titles': {
                    'product': _('Producto'),
                    'quantity': _('Cantidad'),
                    'price': _('Precio'),
                    'total': _('Total'),
                }
            }

        context = {
            'user': seller,
            'my_account_url': get_frontend_url('my_account', get_country_from_language_code(seller.language_code)),
            'mail_nombre_evento': event.title + ' ' + section.name,
            'order_number': instance.identifier,
            'details': details
        }

        context_buyer = {
            'user': buyer,
            'my_account_url': get_frontend_url('my_account', get_country_from_language_code(buyer.language_code)),
            'mail_nombre_evento': event.title + ' ' + section.name,
            'order_number': instance.identifier,
            'details': details
        }
        #if instance.status == 'in_progress':
            #seller
            #send_mail('seller_pending_payment', _('¡ Tenemos un posible Comprador para tus entradas !'), context, 'info@claveglobal.com')
            #buyer
            #send_mail('seller_pending_payment', _('¡ Tenemos un posible Comprador para tus entradas !'), context, 'info@claveglobal.com')
        #el

        if instance.status == 'pending_payment_confirmation':
            send_mail('seller_pending_payment', _('¡ Tenemos un posible Comprador para tus entradas !'), context, seller.email)
        
        elif instance.status == 'paid':
            send_mail('seller_paid', _('¡ Tenemos un posible Comprador para tus entradas !'), context, seller.email)
            send_mail('buyer_pending_payment', _('¡ Tenemos un posible Comprador para tus entradas !'), context_buyer, buyer.email)
        
        elif instance.status == 'confirmed':
            send_mail('buyer_confirmed', _('¡ Tenemos un posible Comprador para tus entradas !'), context_buyer, buyer.email)
        
        elif instance.status == 'completed':
            send_mail('seller_completed', _('Venta Completada'), context, seller.email)
            send_mail('buyer_completed', _('Tu Ticket ha sido entregado!'), context_buyer, buyer.email)
        
        elif instance.status == 'on_transit':
            send_mail('seller_on_transit', _('En Tránsito'), context, context, seller.email)
            send_mail('buyer_on_transit', _('Tu Ticket está en camino!'), context_buyer, context, buyer.email)

        elif instance.status == 'reserved':
            send_mail('buyer_reserved', _('Tu Ticket está reservado!'), context_buyer, buyer.email)
        
        elif instance.status == 'cancelled':
            send_mail('seller_cancelled', _('Lamentablemente una de tus ventas se ha Cancelado.'), context, seller.email)


#{'_state': <django.db.models.base.ModelState object at 0x000001F8D5E1CCD0>, 'id': 29, 'identifier': '2alp44c495', 'created': datetime.datetime(2023, 7, 31, 15, 22, 37, 555708, tzinfo=datetime.timezone.utc), 'modified': datetime.datetime(2023, 8, 4, 22, 9, 29, 162720, tzinfo=datetime.timezone.utc), 'country': 'ar', 'user_id': 18, 'status': 'pending_payment_confirmation', 'billing_address_id': None, 'shipping_address_id': None, 'per_ticket_service_charge': Decimal('6000.00'), 'ticket_price_surcharge_percentage': Decimal('20.00'), 'tickets_subtotal': Decimal('65000.00'), 'service_charge_subtotal': Decimal('6000.00'), 'total': Decimal('71000.00')}

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