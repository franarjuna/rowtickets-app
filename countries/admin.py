from django.contrib import admin

from countries.models import CountrySettings


class CountrySettingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CountrySettings, CountrySettingsAdmin)
