from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "user_type", "is_active", "created_at")
    search_fields = ("email", "name")
    list_filter = ("user_type", "is_active")
    ordering = ("-created_at",)
