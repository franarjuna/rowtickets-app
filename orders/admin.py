from django.contrib import admin

from orders.models import Order, OrderTicket


class OrderTicketInline(admin.TabularInline):
    model = OrderTicket
    readonly_fields = ('ticket', 'quantity', 'price', 'cost', 'subtotal', 'service_charge_subtotal')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderTicketInline]
    extra = 0
    list_display = (
        'identifier', 'status', 'created', 'country', 'tickets_subtotal', 'service_charge_subtotal', 'total'
    )
    readonly_fields = (
        'country', 'user', 'per_ticket_service_charge', 'ticket_price_surcharge_percentage', 'tickets_subtotal',
        'service_charge_subtotal', 'total'
    )

admin.site.register(Order, OrderAdmin)
