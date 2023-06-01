from rest_framework import serializers
from rest_framework.response import Response

from addresses.models import Address

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address 
        fields = '__all__' 