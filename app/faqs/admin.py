from django.contrib import admin
from django.conf import settings
from django import forms

from faqs.models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'country')


admin.site.register(FAQ, FAQAdmin)
