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
    actions = ['create_report']
    extra = 0
    list_display = (
        'identifier', 'quantity', 'price', 'cost', 'ticket','order','order__created'
    )
    list_filter = ('ticket__seller', 'order__identifier', 'order__date', 'order__status', )

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        # Customize this queryset filter based on your requirements
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(order__status='cancelled')
        return queryset
    
    @admin.action(description="Exportar reporte")
    def create_report():
        print('cccc')


admin.site.register(Order, OrderAdmin)
admin.site.register(SellerTicket, SellerTicketAdmin)
