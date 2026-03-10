from django.contrib import admin
from .models import AutomationRule, MessageQueue


@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "business", "trigger_type", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("trigger_type", "is_active")


@admin.register(MessageQueue)
class MessageQueueAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "whatsapp_account", "status", "retry_count", "created_at")
    list_filter = ("status",)