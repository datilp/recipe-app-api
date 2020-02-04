from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # Each of the brackets is a section
    # first argument is the title
    # Note the ('name',) the comma is so python doesn't think
    # it is just a string but an array/tuple?
    # the _('blah') is what? something about json??
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Import dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {'classes': ('wide', ),
                'fields': ('email', 'password1', 'password2')
                }),
    )


admin.site.register(models.User, UserAdmin)
