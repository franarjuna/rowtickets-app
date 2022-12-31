from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.identifiers import generate_random_identifier


class AbstractBaseModel(models.Model):
    identifier = models.CharField(_('identificador'), unique=True, db_index=True, editable=False, max_length=10)
    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.identifier:
            # Generate a unique identifier
            while True:
                self.identifier = generate_random_identifier()

                try:
                    self._meta.model.objects.get(identifier=self.identifier)
                except self._meta.model.DoesNotExist:
                    # Identifier is unique, continue saving the model instance
                    break

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        abstract = True


class CountrySpecificModel(AbstractBaseModel):
    country = models.CharField(_('país'), db_index=True, choices=settings.COUNTRIES, max_length=2)

    class Meta:
        abstract = True


class CountrySpecificUniqueModel(AbstractBaseModel):
    country = models.CharField(_('país'), db_index=True, choices=settings.COUNTRIES, max_length=2, unique=True)

    class Meta:
        abstract = True


class CountrySlugModel(CountrySpecificModel):
    slug = models.SlugField(_('nombre en URL'), max_length=80, allow_unicode=False)

    def clean(self):
        super().clean()

        slug_updated = False

        if not self.pk:
            slug_updated = True
        else:
            old_version = self._meta.model.objects.get(pk=self.pk)

            if old_version.slug != self.slug:
                slug_updated = True

        if slug_updated:
            try:
                self._meta.model.objects.get(country=self.country, slug=self.slug)

                raise ValidationError({
                    'slug': _('Ya existe otro ítem con este nombre en URL para este país')
                })
            except self._meta.model.DoesNotExist:
                pass

    class Meta:
        abstract = True
        unique_together = [['country', 'slug']]
