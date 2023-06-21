from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from countries.areas import get_country_area_name
from rowticket.models import CountrySpecificModel

ADDRESS_TYPES = {
    'BILLING': 'billing',
    'SHIPPING': 'shipping'
}


ADDRESS_TYPE_CHOICES = (
    (ADDRESS_TYPES['BILLING'], _('Facturación')),
    (ADDRESS_TYPES['SHIPPING'], _('Envío'))
)

AR_IVA_CONDITIONS = {
    'CONSUMIDOR_FINAL': 'consumidor_final',
    'RESPONSABLE_INSCRIPTO': 'responsable_inscripto'
}

AR_IVA_CONDITION_CHOICES = (
    (AR_IVA_CONDITIONS['CONSUMIDOR_FINAL'], _('Consumidor Final')),
    (AR_IVA_CONDITIONS['RESPONSABLE_INSCRIPTO'], _('Responsable Inscripto'))
)

class Address(CountrySpecificModel):
    user = models.ForeignKey(
        get_user_model(), related_name='addresses', blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name=_('Usuario')
    )
    address_type = models.CharField(_('tipo de dirección'), max_length=50, choices=ADDRESS_TYPE_CHOICES)

    name = models.CharField(_('Nombre'), max_length=255, blank=True)
    last_name = models.CharField(_('Apellido'), max_length=255, blank=True)
    company_name = models.CharField(_('Nombre de la empresa (opcional)'), max_length=255, blank=True)

    street_address_1 = models.CharField(_('Dirección (línea 1)'), max_length=255, blank=True)
    street_address_2 = models.CharField(_('Dirección (línea 2)'), max_length=255, blank=True)
    city = models.CharField(_('Ciudad / Localidad'), max_length=255, blank=True)
    country_area = models.CharField(_('Estado / Provincia / Región'), max_length=255, blank=True)
    postal_code = models.CharField(_('Código postal'), max_length=64, blank=True)

    phone = models.CharField(_('Teléfono'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), max_length=30, blank=True)

    # Country-specific fields
    # Argentina
    ar_dni = models.CharField(_('DNI'), max_length=100, blank=True)
    ar_iva_condition = models.CharField(
        _('Condición frente al IVA'), max_length=100, choices=AR_IVA_CONDITION_CHOICES, blank=True
    )

    # Chile
    cl_rut = models.CharField(_('RUT'), max_length=100, blank=True)

    def __str__(self):
        return self.full_street

    @property
    def full_name(self):
        return '{} {}'.format(self.name, self.last_name)

    @property
    def full_street(self):
        street = self.street_address_1

        if self.street_address_2:
            street = '{} {}'.format(street, self.street_address_2)

        return street

    def get_country_area(self):
        return get_country_area_name(self.country, self.country_area)

    class Meta:
        verbose_name = _('Dirección')
        verbose_name_plural = _('Direcciones')
        ordering = (
            '-created',
        )
