from django.contrib import admin

from fiserv_payments.models import FiservIPN, FiservPaymentMethod, FiservPayment


class FiservIPNInline(admin.StackedInline):
    readonly_fields = ('data', 'created', 'modified')
    extra = 0
    model = FiservIPN


class FiservPaymentMethodAdmin(admin.ModelAdmin):
    fields = ('country', 'display_name', 'active', 'api_key', 'access_token', 'test_mode')
    list_display = ('display_name', 'country', 'identifier')


class FiservPaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order', 'checkout_id', 'request_data', 'response_data', 'created', 'modified'
    )
    list_display = ('__str__', 'payment_method', 'checkout_id', 'order', 'created', 'modified')
    inlines=[FiservIPNInline]


admin.site.register(FiservPaymentMethod, FiservPaymentMethodAdmin)
admin.site.register(FiservPayment, FiservPaymentAdmin)
