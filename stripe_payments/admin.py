from django.contrib import admin

from stripe_payments.models import StripeIPN, StripePaymentMethod, StripePayment


class StripeIPNInline(admin.StackedInline):
    readonly_fields = ('data', 'created', 'modified')
    extra = 0
    model = StripeIPN


class StripePaymentMethodAdmin(admin.ModelAdmin):
    fields = ('country', 'display_name', 'active', 'api_key', 'access_token', 'test_mode')
    list_display = ('display_name', 'country', 'identifier')


class StripePaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order', 'checkout_id', 'request_data', 'response_data', 'created', 'modified'
    )
    list_display = ('__str__', 'payment_method', 'checkout_id', 'order', 'created', 'modified')
    inlines=[StripeIPNInline]


admin.site.register(StripePaymentMethod, StripePaymentMethodAdmin)
admin.site.register(StripePayment, StripePaymentAdmin)
