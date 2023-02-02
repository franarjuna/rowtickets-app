from django.conf import settings
from django.core import validators
from django.db import models


class LanguageCodeField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = settings.LANGUAGES
        kwargs['default'] = settings.LANGUAGE_CODE
        kwargs['max_length'] = 10

        super().__init__(*args, **kwargs)
