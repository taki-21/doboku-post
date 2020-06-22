from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """管理画面に表示する項目"""
    list_display = (
        'username', 'email'
    )

    fieldsets = [
        (None, {'fields': ['username', 'password']}),
        ('PersonalInfo', {'fields': ['email', 'introduction', 'icon_image', 'home_image']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important dates', {'fields': ['last_login', 'date_joined']}),
    ]


admin.site.register(CustomUser, CustomUserAdmin)
