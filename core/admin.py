from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "user_type", "is_verified", "is_staff")
    list_filter = ("user_type", "is_verified", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("user_type", "is_verified", "verification_code")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("email", "user_type")}),
    )
