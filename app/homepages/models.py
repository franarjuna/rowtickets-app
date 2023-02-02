from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from rowticket.models import AbstractBaseModel, CountrySpecificUniqueModel


class Homepage(CountrySpecificUniqueModel):
    sell_module_title = models.CharField(
        _('módulo vender: título'), max_length=150,
        default='Vende con tranquilidad'
    )
    sell_module_text = models.TextField(
        _('módulo vender: texto'),
        default='Establece el precio y ajústalo en cualquier momento antes de que se vendan tus entradas. La entrega '
            'es rápida y sin complicaciones seguida del pago puntual. Manejamos las comunicaciones con los compradores.'
    )
    sell_module_button_text = models.CharField(
        _('módulo vender: texto botón'), max_length=80, default='Vender entradas'
    )
    warranty_module_buy_sell_text = models.CharField(
        _('módulo garantía: texto compra venta'), max_length=150,
        default='Compra y vende con confianza'
    )
    warranty_module_customer_service_text = models.CharField(
        _('módulo garantía: texto servicio al cliente'), max_length=150,
        default='Servicio al cliente hasta su asiento'
    )
    warranty_module_warranty_text = models.CharField(
        _('módulo garantía: texto garantía'), max_length=150,
        default='Cada pedido está 100% garantizado'
    )
    about_us_module_heading = models.CharField(
        _('módulo quienes somos: encabezado'), max_length=150,
        default='Nosotros y nuestros partners'
    )
    about_us_module_title = models.CharField(
        _('módulo quienes somos: título'), max_length=150,
        default='Más de 20 años de experiencia'
    )
    about_us_module_subtitle = models.CharField(
        _('módulo quienes somos: subtítulo'), max_length=150,
        default='Somos un grupo de profesionales a tu servicio.'
    )
    about_us_module_text = models.TextField(
        _('módulo quienes somos: texto'),
        default='RowTicket es la plataforma de compra y venta secundaria de entradas. Con entradas disponibles '
        'para eventos deportivos, musicales y de teatro, en todo Latam.'
    )
    about_us_module_button_text = models.CharField(_('módulo quienes somos: texto botón'), max_length=150, default='Conocenos')
    contact_us_module_event_today = models.CharField(
        _('módulo contacto: ¿el evento es hoy?'),
        max_length=100, default='¿El evento es hoy?'
    )
    contact_us_module_text = models.TextField(
        _('módulo contacto: texto'), default='Por consultas o ventas coorporativas contactate con nosotros'
    )

    def __str__(self):
        return f'{self.get_country_display()}'

    class Meta:
        verbose_name = _('página principal')
        verbose_name_plural = _('páginas principales')
        ordering = ('country', )


class HomepageSlide(AbstractBaseModel):
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE, related_name='slides')
    date_text = models.CharField(_('texto fecha'), max_length=150, blank=True)
    venue_text = models.CharField(_('texto sede'), max_length=150, blank=True)
    button_text = models.CharField(_('texto botón'), max_length=100)
    event = models.ForeignKey(
        'events.Event', verbose_name=_('evento'), on_delete=models.CASCADE, related_name='homepage_slides',
        blank=True, null=True
    )
    organizer = models.ForeignKey(
        'events.Organizer', verbose_name=_('organizador'), on_delete=models.CASCADE, related_name='homepage_slides',
        blank=True, null=True
    )
    link = models.URLField(_('link'), blank=True)

    image = models.ImageField(
        _('imagen'), upload_to='event_gallery_images',
        width_field='image_width', height_field='image_height'
    )

    image_width = models.PositiveIntegerField(_('ancho de imagen'), null=True, blank=True)
    image_height = models.PositiveIntegerField(_('alto de imagen'), null=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    image_large = ImageSpecField(source='image', processors=[ResizeToFill(1920, 900)], format='JPEG')

    def clean(self):
        if not self.event and not self.organizer and not self.link:
            raise ValidationError(_('Por favor especifique un evento, organizador o link'))

        if ((bool(self.event) + bool(self.organizer) + bool(self.link)) > 1):
            raise ValidationError(_('Por favor especifica sólo un ítem entre evento, organizador y link'))

    class Meta:
        verbose_name = _('slide')
        verbose_name_plural = _('slides')
        ordering = ('homepage', 'order')
