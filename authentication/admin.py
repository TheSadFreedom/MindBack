from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "updated_at", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    fields = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "logo",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
