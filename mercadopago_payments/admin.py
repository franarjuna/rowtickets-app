from django.contrib import admin

from mercadopago_payments.models import MercadoPagoPaymentMethod


class MercadoPagoPaymentMethodAdmin(admin.ModelAdmin):
    fields = ('country', 'display_name', 'active', 'access_token', 'public_key')
    list_display = ('display_name', 'country', 'identifier')


admin.site.register(MercadoPagoPaymentMethod, MercadoPagoPaymentMethodAdmin)
