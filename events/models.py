from django.db import models
from django.db.models import Case, F, OuterRef, Subquery, Sum, Value, When
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from orders.models import ORDER_STATUSES
from rowticket.models import AbstractBaseModel, CountrySlugModel
from django_better_admin_arrayfield.models.fields import ArrayField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

COLOR_CHOICES = [
    ('blue', _('Azul')),
    ('green', _('Verde')),
    ('orange', _('Naranja')),
    ('pink', _('Rosa')),
    ('red', _('Rojo'))
]

TICKET_TYPES = [
    ('paper', _('Papel')),
    ('e_ticket', _('E Ticket')),
    ('electronic_ticket_transfer', _('Transferencia de entradas electrónicas'))
]

SELLING_CONDITIONS = (
    ('no_preference', _('Sin preferencia')),
    ('sold_together', _('Se venden juntas')),
    ('no_single_ticket_unsold', _('No dejar 1 sin vender')),
    ('sold_by_pairs', _('Se venden de a pares'))
)


class Category(CountrySlugModel):
    name = models.CharField(_('nombre'), max_length=150)
    published = models.BooleanField(_('publicada'), default=True)
    color = models.CharField(_('color'), max_length=20, choices=COLOR_CHOICES)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    # Images
    header_image = models.ImageField(
        _('imagen de cabecera'), upload_to='category_header_images',
        width_field='header_image_width', height_field='header_image_height'
    )
    header_image_width = models.PositiveIntegerField(_('ancho de imagen de cabecera'), null=True, blank=True)
    header_image_height = models.PositiveIntegerField(_('alto de imagen de cabecera'), null=True, blank=True)

    # ImageKit specs
    header_image_large = ImageSpecField(
        source='header_image', processors=[ResizeToFill(1920, 470)], format='JPEG'
    )

    def __str__(self):
        return f'{self.name} - {self.get_country_display()}'

    class Meta:
        verbose_name = _('categoría')
        verbose_name_plural = _('categorías')
        ordering = ('country', 'order', )


class Venue(CountrySlugModel):
    name = models.CharField(_('nombre'), max_length=150)
    address = models.CharField(_('dirección'), max_length=200, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('sede')
        verbose_name_plural = _('sedes')


class Organizer(CountrySlugModel):
    name = models.CharField(_('nombre'), max_length=150)
    twitter_handle = models.CharField(_('usuario de Twitter'), max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('organizador')
        verbose_name_plural = _('organizadores')


class EventManager(models.Manager):
    def with_starting_price(self):
        starting_ticket_price = Ticket.objects.with_availability().order_by('price').filter(
            available_quantity__gt=0, event_id=OuterRef('pk')
        )

        return self.annotate(
            starting_price=Subquery(starting_ticket_price.values('price')[:1])
        )


class Event(CountrySlugModel):
    title = models.CharField(_('nombre'), max_length=150)
    category = models.ForeignKey(
        Category, verbose_name=_('categoría'), on_delete=models.PROTECT, related_name='events'
    )
    organizer = models.ForeignKey(
        Organizer, verbose_name=_('organizador'), on_delete=models.PROTECT, related_name='events', null=True, blank=True
    )
    date = models.DateTimeField(_('fecha y hora'), db_index=True)
    date_text = models.CharField(_('fecha (texto)'), max_length=150, blank=True)
    venue = models.ForeignKey(
        Venue, verbose_name=_('sede'), on_delete=models.PROTECT, null=True, blank=True, related_name='events'
    )
    online_event = models.BooleanField(_('evento online'), default=False)
    highlighted = models.BooleanField(_('destacado'), default=False)
    published = models.BooleanField(_('publicado'), default=False)

    
    pay_date = models.DateField(_('dia de liquidacion'), db_index=True, null=True, blank=True)

    individual_percentage = models.DecimalField(_('coeficiente de venta especial'), max_digits=5, decimal_places=2, null=True, blank=True)


    # Images
    main_image = models.ImageField(
        _('imagen principal'), upload_to='event_main_images',
        width_field='main_image_width', height_field='main_image_height'
    )
    main_image_width = models.PositiveIntegerField(_('ancho de imagen principal'), null=True, blank=True)
    main_image_height = models.PositiveIntegerField(_('alto de imagen principal'), null=True, blank=True)

    # ImageKit specs
    main_image_large = ImageSpecField(source='main_image', processors=[ResizeToFit(1920, 1920)], format='JPEG')
    main_image_thumb = ImageSpecField(source='main_image', processors=[ResizeToFill(300, 300)], format='JPEG')

    objects = EventManager()
    
    @property
    def formatted_date(self):
        return self.date.strftime('%d/%m/%Y  %H:%M')


    def __str__(self):
        return f'{self.title}'

    def clean(self):
        if not self.online_event and not self.venue:
            raise ValidationError({
                'venue': _('Seleccione una sede para el evento presencial')
            })

    class Meta:
        verbose_name = _('evento')
        verbose_name_plural = _('eventos')
        ordering = ('-date', )


class EventImage(AbstractBaseModel):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.CASCADE, related_name='event_images'
    )
    image = models.ImageField(
        _('imagen'), upload_to='event_images',
        width_field='image_width', height_field='image_height'
    )
    image_width = models.PositiveIntegerField(_('ancho'), null=True, blank=True)
    image_height = models.PositiveIntegerField(_('alto'), null=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    image_large = ImageSpecField(source='image', processors=[ResizeToFit(800, 800)], format='JPEG')
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFit(180, 180)], format='JPEG')

    class Meta:
        verbose_name = _('imagen de evento')
        verbose_name_plural = _('imágenes de evento')
        ordering = ('event', 'order')


class EventGalleryImage(AbstractBaseModel):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.CASCADE, related_name='event_gallery_images'
    )
    image = models.ImageField(
        _('imagen'), upload_to='event_gallery_images',
        width_field='image_width', height_field='image_height'
    )
    image_width = models.PositiveIntegerField(_('ancho'), null=True, blank=True)
    image_height = models.PositiveIntegerField(_('alto'), null=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    image_large = ImageSpecField(source='image', processors=[ResizeToFit(800, 800)], format='JPEG')
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFit(180, 180)], format='JPEG')

    class Meta:
        verbose_name = _('imagen de galería de evento')
        verbose_name_plural = _('imágenes de galería de evento')
        ordering = ('event', 'order')

class Section(AbstractBaseModel,DynamicArrayMixin):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.CASCADE, related_name='sections'
    )
    name = models.CharField(_('nombre'), max_length=150)
    sub_section = ArrayField(models.TextField(_('sub-sector')), null=True, blank=True)
    #ArrayField(_('sub-sector'), help_text="This is the grey text", default='', blank=True)
    color = ColorField(verbose_name=_('color'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('sectores del evento')
        verbose_name_plural = _('sectores del evento')
        ordering = ('event', 'name')


class TicketManager(models.Manager):
    def with_availability(self):
        return self.annotate(
            sold_quantity=Sum(
                Case(
                    When(order_tickets__order__status__in=[
                        ORDER_STATUSES['PENDING_PAYMENT_CONFIRMATION'],
                        ORDER_STATUSES['PAID']
                    ], then='order_tickets__quantity'),
                    output_field=models.PositiveIntegerField(),
                    default=Value(0)
                )
            )
        ).annotate(
            available_quantity=F('quantity')-F('sold_quantity')
        )


class Ticket(AbstractBaseModel):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.PROTECT, related_name='tickets'
    )
    seller = models.ForeignKey(
        'users.User', verbose_name=_('vendedor'), on_delete=models.PROTECT, related_name='tickets'
    )

    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name=_('sector'))
    subsection = models.CharField(_('subsector'), max_length=50, default='', blank=True, null=True)
    price = models.DecimalField(_('precio final'), max_digits=10, decimal_places=2)
    cost = models.DecimalField(_('precio'), max_digits=10, decimal_places=2)
    ticket_type = models.CharField(_('tipo de entrada'), choices=TICKET_TYPES, max_length=50)
    row = models.CharField(_('fila'), max_length=50, default='', blank=True, null=True)
    ready_to_ship = models.BooleanField(_('listo para enviar'))
    ready_date = models.DateField(_('dia de disponibilidad'), null=True, blank=True)
    extra_info = models.CharField(_('información extra'), max_length=255, blank=True)
    quantity = models.PositiveIntegerField(_('cantidad'))
    selling_condition = models.CharField(
        _('condición de venta'), max_length=50, choices=SELLING_CONDITIONS, default='no_preference'
    )
    status =  models.BooleanField(_('status'), default=True)

    attachment = models.ImageField(_('imagen'), default='', null=True, blank=True)

    objects = TicketManager()

    def __str__(self):
        return f'{self.event}: {self.section} {self.subsection} {self.price} ({self.seller.email})'

    class Meta:
        verbose_name = _('entradas')
        verbose_name_plural = _('entradas')
        ordering = ('event', 'price')
