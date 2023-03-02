from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from rowticket.models import AbstractBaseModel, CountrySlugModel


COLOR_CHOICES = [
    ('blue', _('Azul')),
    ('green', _('Verde')),
    ('orange', _('Naranja')),
    ('pink', _('Rosa')),
    ('red', _('Rojo'))
]


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
        return f'{self.name}'

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


class Event(CountrySlugModel):
    title = models.CharField(_('nombre'), max_length=150)
    category = models.ForeignKey(
        Category, verbose_name=_('categoría'), on_delete=models.PROTECT, related_name='events'
    )
    date = models.DateTimeField(_('fecha y hora'), db_index=True)
    date_text = models.CharField(_('fecha (texto)'), max_length=150, blank=True)
    venue = models.ForeignKey(
        Venue, verbose_name=_('sede'), on_delete=models.PROTECT, null=True, blank=True, related_name='events'
    )
    online_event = models.BooleanField(_('evento online'), default=False)
    highlighted = models.BooleanField(_('destacado'), default=False)
    published = models.BooleanField(_('publicado'), default=False)

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
class EventPlaces(AbstractBaseModel):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.CASCADE, related_name='event_places'
    )
    title = models.CharField(_('nombre'), max_length=150)
    color = models.CharField(_('color'), max_length=7)

    class Meta:
        verbose_name = _('sectores del evento')
        verbose_name_plural = _('sectores del evento')
        ordering = ('event', 'title')
class EventTickets(AbstractBaseModel):
    event = models.ForeignKey(
        Event, verbose_name=_('evento'), on_delete=models.CASCADE, related_name='event_tickets'
    )
    user = models.ForeignKey(
        Category, verbose_name=_('vendedor'), on_delete=models.PROTECT, related_name='ticket_seller', null=True, blank=True
    )

    title = models.CharField(_('fila'), max_length=150)
    price = models.DecimalField(_('precio_final'), max_digits=10, decimal_places=2)
    cost = models.DecimalField(_('precio'), max_digits=10, decimal_places=2)
    ready_to_go = models.BooleanField(_('ready_to_go'))
    add_info = models.TextField(_('add_info'))

    class Meta:
        verbose_name = _('entradas a la venta')
        verbose_name_plural = _('entradas a la venta')
        ordering = ('event', 'price')
