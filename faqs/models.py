from django.db import models
from django.utils.translation import gettext_lazy as _

from django_quill.fields import QuillField

from rowticket.models import CountrySpecificModel


class FAQ(CountrySpecificModel):
    question = models.CharField(_('pregunta'), max_length=255)
    answer = QuillField(verbose_name=_('respuesta'), blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('pregunta frecuente')
        verbose_name_plural = _('preguntas frecuentes')
        ordering = ('country', 'order', )
        unique_together = ('country', 'order')
