from django.contrib import admin
from .models import (
    ActivityLog,
    Notification,
    WebhookLog,
    APILog,
    AIResponseLog
)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "business", "action", "created_at")
    list_filter = ("action",)
    search_fields = ("user__email",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "business", "type", "is_read", "created_at")
    list_filter = ("type", "is_read")


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "event_type", "processed", "created_at")
    list_filter = ("processed",)


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint", "status_code", "created_at")


@admin.register(AIResponseLog)
class AIResponseLogAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "conversation", "tokens_used", "created_at")