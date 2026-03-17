from django.contrib import admin
from .models import (
    Lead,
    Conversation,
    Message,
    MediaFile,
    Tag,
    ConversationTag,
    AgentAssignment
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "business", "is_blocked", "last_message_at")
    search_fields = ("phone_number", "name")
    list_filter = ("is_blocked",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "business", "status", "last_message_at")
    list_filter = ("status",)
    search_fields = ("lead__phone_number",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "direction",
        "message_type",
        "status",
        "send_by",
        "timestamp",
    )
    list_filter = ("direction", "message_type", "status")
    search_fields = ("content",)


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "media_type", "created_at")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "business", "color")


@admin.register(ConversationTag)
class ConversationTagAdmin(admin.ModelAdmin):
    list_display = ("conversation", "tag")


@admin.register(AgentAssignment)
class AgentAssignmentAdmin(admin.ModelAdmin):
    list_display = ("conversation", "agent", "assigned_at", "status")