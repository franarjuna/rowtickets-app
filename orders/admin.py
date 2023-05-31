from django.contrib import admin

from orders.models import Order, OrderTicket


class OrderTicketInline(admin.StackedInline):
    model = OrderTicket


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderTicketInline]
    extra = 0
    list_display = ('identifier', 'status', 'created', 'country')

admin.site.register(Order, OrderAdmin)
