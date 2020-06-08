from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Category, CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age',)}),)
    list_display = ['username', 'email', 'age']

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CustomUser, CustomUserAdmin)
