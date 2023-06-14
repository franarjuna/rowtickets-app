from django.contrib import admin

from orders.models import Order, OrderTicket, SellerTicket


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
    list_filter = ('identifier', 'status', 'user', 'created', 'country', )
    

class SellerTicketAdmin(admin.ModelAdmin):
    extra = 0
    list_display = (
        'identifier', 'quantity', 'price', 'cost', 'ticket'
    )
    list_filter = ('ticket__seller', )
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Order, OrderAdmin)
admin.site.register(SellerTicket, SellerTicketAdmin)
