from operator import itemgetter

from rest_framework import mixins, viewsets
from rest_framework import permissions, status
from rest_framework.response import Response

from events.models import Ticket
from orders.models import Order, OrderTicket, ORDER_STATUSES
from orders.serializers import OrderCreateSerializer, OrderSerializer


class OrderViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    lookup_field = 'identifier'
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
        self.request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        ticket_qs = Ticket.objects.with_availability()

        tickets_not_found = []
        tickets_with_lower_availability = []

        order_tickets = data.pop('order_tickets')

        for index, ticket_data in enumerate(order_tickets):
            ticket_identifier, quantity = itemgetter('ticket_identifier', 'quantity')(ticket_data)

            try:
                ticket = ticket_qs.get(identifier=ticket_identifier)

                if ticket.available_quantity < quantity:
                    tickets_with_lower_availability.append({
                        ticket_identifier: ticket.available_quantity
                    })

                order_tickets[index]['id'] = ticket.id

            except Ticket.DoesNotExist:
                tickets_not_found.append(ticket_data['ticket_identifier'])

        if (len(tickets_not_found) > 0 or len(tickets_with_lower_availability) > 0):
            return Response({
                'tickets_not_found': tickets_not_found,
                'tickets_with_lower_availability': tickets_with_lower_availability
            }, status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, status=ORDER_STATUSES['IN_PROGRESS'])

        for ticket_data in order_tickets:
            OrderTicket.objects.create(order=order, ticket_id=ticket_data['id'], quantity=ticket_data['quantity'])

        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def validate(self, data):
    #     ticket_qs = Ticket.objects.with_availability()

    #     target_tickets = ticket_qs.filter(identifier__in=map(lambda t: t['ticket_identifier'], data['order_tickets']))

    #     if (len(target_tickets) !== len(data['order_tickets')]):
    #         # Some ticket could not be found or is unavailable
    #         raise serializer.ValidationError()

    #     return super().create(request, *args, **kwargs)
