from django.contrib import admin
from .models import App, WhatsAppAccount
from django.db import models
from django import forms
from django_json_widget.widgets import JSONEditorWidget


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "app_id", "is_active", "created_at")
    search_fields = ("name", "app_id")
    
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(WhatsAppAccount)
class WhatsAppAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "business",
        "display_phone_number",
        "waba_id",
        "quality_rating",
        "messaging_limit_tier",
        "is_active",
    )
    search_fields = ("display_phone_number", "waba_id")
    list_filter = ("is_active",)