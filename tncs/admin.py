from django.contrib import admin
from django.conf import settings
from django import forms

from tncs.models import TnC


class TnCAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'country')


admin.site.register(TnC, TnCAdmin)
