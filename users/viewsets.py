from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rowticket.decorators import query_debugger_detailed

from events.serializers import TicketSerializer
from users.serializers import AccountSerializer
from orders.serializers import OrderSerializer
from users.models import User
from events.models import Ticket
from orders.models import Order

class AccountViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountSerializer

        return AccountSerializer

    def list(self, request, *args, **kwargs): 
        
        queryset = super().get_queryset()

        queryset = queryset.filter(id=request.user.id)
        #queryset = queryset.filter(country=self.kwargs['country_country'])
        serializer = self.get_serializer(queryset, many=True)
        response = {
            'dashboard': serializer.data
        }
        return Response(response)



class PurchasesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderSerializer

        return OrderSerializer

    def list(self, request, *args, **kwargs): 
        
        queryset = super().get_queryset()

        queryset = queryset.filter(country=self.kwargs['country_country'],user=request.user)
        #queryset = queryset.filter(country=self.kwargs['country_country'])
        serializer = self.get_serializer(queryset, many=True)
        response = {
            'total': 0,
            'data': serializer.data
        }
        return Response(response)

class OnSaleViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketSerializer

        return TicketSerializer

    def list(self, request, *args, **kwargs): 
        
        queryset = super().get_queryset()

        queryset = queryset.filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            'total': 0,
            'data': serializer.data
        }
        return Response(response)