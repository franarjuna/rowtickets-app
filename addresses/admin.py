from django.contrib import admin

from addresses.models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'address_type', 'country')
    list_filter = ('country', )


admin.site.register(Address, AddressAdmin)
