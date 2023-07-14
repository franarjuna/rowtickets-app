from django.contrib import admin

from viumi_payments.models import ViumiIPN, ViumiPaymentMethod, ViumiPayment


class ViumiIPNInline(admin.StackedInline):
    readonly_fields = ('data', 'created', 'modified')
    extra = 0
    model = ViumiIPN


class ViumiPaymentMethodAdmin(admin.ModelAdmin):
    fields = ('country', 'display_name', 'active', 'api_key', 'access_token', 'test_mode')
    list_display = ('display_name', 'country', 'identifier')


class ViumiPaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order', 'checkout_id', 'request_data', 'response_data', 'created', 'modified'
    )
    list_display = ('__str__', 'payment_method', 'checkout_id', 'order', 'created', 'modified')
    inlines=[ViumiIPNInline]


admin.site.register(ViumiPaymentMethod, ViumiPaymentMethodAdmin)
admin.site.register(ViumiPayment, ViumiPaymentAdmin)
