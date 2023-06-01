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
        fields = ('identifier', 'status', 'order_tickets', )
