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
