from django.db import models
from django.utils.translation import gettext_lazy as _

from django_quill.fields import QuillField

from rowticket.models import CountrySpecificModel


class TnC(CountrySpecificModel):
    title = models.CharField(_('título'), max_length=150)
    content = QuillField(verbose_name=_('contenido'))
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('término')
        verbose_name_plural = _('términos y condiciones')
        ordering = ('country', 'order', )
        unique_together = ('country', 'order')
