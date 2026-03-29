from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "phone_number", "is_staff", "is_active", "is_email_verified")
    search_fields = ("email", "username", "phone_number")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "first_name", "last_name", "phone_number", "date_of_birth", "profile_picture")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "is_email_verified", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "date_joined", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
