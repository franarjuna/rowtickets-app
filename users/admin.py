from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserAdmin(DjangoUserAdmin):
    ordering = ('last_name', 'first_name', )
    list_display = ('identifier', 'language_code', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'created', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Fechas importantes'), {'fields': ('created', 'modified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name', 'email', 'language_code', 'password1', 'password2',
                'is_staff', 'is_superuser', 'is_superuser'
            ),
        }),
    )
    readonly_fields = ('created', 'modified', )
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email', )

admin.site.register(User, UserAdmin)
