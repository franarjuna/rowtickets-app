from rest_framework import serializers

from events.models import Ticket
from orders.models import Order, OrderTicket, ORDER_STATUSES
from rowticket.serializer_fields import IdentifierField
from events.serializers import TicketCreateSerializer


class OrderTicketCreateSerializer(serializers.ModelSerializer):
    ticket_identifier = IdentifierField()

    class Meta:
        model = OrderTicket
        fields = ('ticket_identifier', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    order_tickets = OrderTicketCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('order_tickets', )

class OrderTicketSerializer(serializers.ModelSerializer):
    ticket = TicketCreateSerializer()
    class Meta:
        model = OrderTicket
        fields = ('identifier', 'quantity','ticket')


class OrderSerializer(serializers.ModelSerializer):
    order_tickets = OrderTicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ('identifier', 'created', 'status', 'order_tickets','per_ticket_service_charge','ticket_price_surcharge_percentage','tickets_subtotal','service_charge_subtotal','total','status' )


class OrderSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('identifier', 'created', 'status','per_ticket_service_charge','ticket_price_surcharge_percentage','tickets_subtotal','service_charge_subtotal','total','status' )


class OrderTicketListSerializer(serializers.ModelSerializer):
    ticket = TicketCreateSerializer()
    order = OrderSmallSerializer()
    class Meta:
        model = OrderTicket
        fields = ('identifier', 'quantity','ticket','order')

