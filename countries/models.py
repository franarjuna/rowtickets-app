from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.models import CountrySpecificUniqueModel


class CountrySettings(CountrySpecificUniqueModel):
    per_ticket_service_charge = models.DecimalField(
        _('service charge'), max_digits=10, decimal_places=2
    )
    ticket_price_surcharge_percentage = models.DecimalField(
        _('cargo plataforma (porcentaje sobre precio vendedor)'), max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.get_country_display()

    class Meta:
        verbose_name = _('configuración de país')
        verbose_name_plural = _('configuraciones de país')
