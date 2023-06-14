from django.contrib import admin

from mobbex_payments.models import MobbexIPN, MobbexPaymentMethod, MobbexPayment


class MobbexIPNInline(admin.StackedInline):
    readonly_fields = ('data', 'created', 'modified')
    extra = 0
    model = MobbexIPN


class MobbexPaymentMethodAdmin(admin.ModelAdmin):
    fields = ('country', 'display_name', 'active', 'api_key', 'access_token', 'test_mode')
    list_display = ('display_name', 'country', 'identifier')


class MobbexPaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order', 'checkout_id', 'request_data', 'response_data', 'created', 'modified'
    )
    list_display = ('__str__', 'payment_method', 'checkout_id', 'order', 'created', 'modified')
    inlines=[MobbexIPNInline]


admin.site.register(MobbexPaymentMethod, MobbexPaymentMethodAdmin)
admin.site.register(MobbexPayment, MobbexPaymentAdmin)
