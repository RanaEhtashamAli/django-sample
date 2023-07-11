from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdminCustomized(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_role',)}),
    )


admin.site.register(User, UserAdminCustomized)
