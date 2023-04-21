from django.conf import settings
from django.utils.translation import gettext_lazy as _

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from allauth.account.utils import setup_user_email
from rest_framework import serializers

from countries.utils import get_language_code_from_country
from orders.models import Order
from users.models import User
from orders.serializers import OrderSerializer
from events.serializers import TicketSerializer

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    country = serializers.ChoiceField(required=True, choices=list(settings.COUNTRY_LANGUAGES.keys()))

    def validate_email(self, email):
        email = get_adapter().clean_email(email)

        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('Ya existe un usuario con este email.'),
                )

        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(_('Las dos contraseñas no coinciden'))

        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'country': self.validated_data.get('country', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        if 'password' in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )

        user.language_code = get_language_code_from_country(self.cleaned_data['country'])
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        return user

class AccountSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name','orders','tickets')
        #fields = ('first_name', 'last_name')