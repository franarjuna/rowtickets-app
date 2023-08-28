from django.contrib import admin

from orders.models import Order, OrderTicket, SellerTicket


class OrderTicketInline(admin.TabularInline):
    model = OrderTicket
    readonly_fields = ('ticket', 'quantity', 'price', 'cost', 'subtotal', 'service_charge_subtotal')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    actions = ['canelar_masivo']
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

    @admin.action(description="Cancelar evento(s) seleccionado")
    def canelar_masivo(modeladmin, request, queryset):
        for book in queryset:
            book.status = 'cancelled'
            book.save()

class SellerTicketAdmin(admin.ModelAdmin):
    extra = 0
    list_display = (
        'identifier', 'quantity', 'price', 'cost', 'ticket','order'
    )
    list_filter = ('ticket__seller', 'order__identifier', 'order__status', )

    def has_add_permission(self, request, obj=None):
        return False



admin.site.register(Order, OrderAdmin)
admin.site.register(SellerTicket, SellerTicketAdmin)
