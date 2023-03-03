from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from rowticket.fields import LanguageCodeField
from rowticket.models import AbstractBaseModel


class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, password=None
    ):
        if not email:
            raise ValueError(_('El campo email es obligatorio'))

        if not first_name:
            raise ValueError(_('El campo nombre es obligatorio'))

        if not last_name:
            raise ValueError(_('El campo apellido es obligatorio'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email, first_name, last_name, password=None
    ):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('nombre'), max_length=100)
    last_name = models.CharField(_('apellido'), max_length=100)

    is_staff = models.BooleanField(_('es staff'), default=False)
    is_active = models.BooleanField(_('activo'), default=True)
    is_seller = models.BooleanField(_('venta autorizada'), default=False)
    language_code = LanguageCodeField(_('código de idioma'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    get_full_name.short_description = _('nombre completo')
    get_full_name.admin_order_field = ('last_name', )

    def get_short_name(self):
        return self.first_name

    def clean(self):
        if self.email:
            queryset = User.objects.all()

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            try:
                queryset.get(email__iexact=self.email)

                raise ValidationError({
                    'email': _('Ya existe un usuario con este email')
                })

            except User.DoesNotExist:
                pass

        self.email = self.email.lower()

        return super().clean()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
