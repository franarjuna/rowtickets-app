from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rowticket.decorators import query_debugger_detailed
from rest_framework import pagination
from events.serializers import TicketSerializer
from users.serializers import AccountSerializer
from orders.serializers import OrderSerializer, OrderTicketListSerializer
from addresses.serializers import AddressesSerializer
from users.models import User
from events.models import Ticket
from orders.models import Order,OrderTicket
from addresses.models import Address

class AccountViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountSerializer

        return AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'partial_update' or self.action == 'update':
            data = queryset.filter(pk=self.request.user.id)
            print(data)
            return data
        else:
            return queryset.filter(published=True, country=self.kwargs['country_country'])

    def list(self, request, *args, **kwargs):
        queryset = super().get_queryset()

        queryset = queryset.filter(id=request.user.id)
        #queryset = queryset.filter(country=self.kwargs['country_country'])
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "data":serializer.data
        }
        return Response(response)

    def partial_update(self, request, pk, *args, **kwargs):
        partial = True
        #request.user.id
        filter = {}
        queryset = self.get_queryset()

        instance = get_object_or_404(queryset, **filter)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PurchasesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderSerializer

        return OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = super().get_queryset()

        queryset = queryset.filter(country=self.kwargs['country_country'],user=request.user, status__in=['paid','reserved','approved','completed'])
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
        queryset = Ticket.objects.with_availability().all()

        queryset = queryset.filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            'total': 0,
            'data': serializer.data
        }
        return Response(response)

class SoldViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OrderTicket.objects.all()
    pagination.PageNumberPagination.page_size = 10

    def get_serializer_class(self):
        return OrderTicketListSerializer

    def list(self, request, *args, **kwargs):
        queryset = OrderTicket.objects.filter(ticket__seller=request.user, order__status__in=['paid','reserved','approved','completed']).exclude(order__status='cancelled')

        serializer = self.get_serializer(queryset, many=True)
        response = {
            'total': queryset.count(),
            'data': serializer.data
        }

        return Response(response)


class AddressesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Address.objects.all()

    def get_serializer_class(self):
        return AddressesSerializer

    def list(self, request, *args, **kwargs):
        my_adresses = AddressesSerializer(Address.objects.filter(user=request.user), many=True).data
        return Response(my_adresses)
