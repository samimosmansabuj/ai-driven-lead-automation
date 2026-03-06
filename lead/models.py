from core.models import BaseModel
from core.choice_select import MESSAGE_DIRECTION, MESSAGE_TYPE, MESSAGE_STATUS, CONVERSATION_STATUS, CONVERSATION_SOURCE
from django.db import models
import uuid

class Lead(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="lead", blank=True, null=True)
    whatsapp_account = models.ForeignKey('integration.WhatsAppAccount', on_delete=models.SET_NULL, related_name="lead", blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    profile_pic = models.URLField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('business', 'phone_number')
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['business', 'phone_number'])
        ]

class Conversation(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="conversations", blank=True, null=True)
    whatsapp_account = models.ForeignKey('integration.WhatsAppAccount', on_delete=models.SET_NULL, related_name="conversations", blank=True, null=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="conversations")
    last_message = models.TextField(null=True, blank=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CONVERSATION_STATUS.choices, default=CONVERSATION_STATUS.OPEN)
    source = models.CharField(max_length=20, choices=CONVERSATION_SOURCE.choices, default=CONVERSATION_SOURCE.WHATSAPP)

    class Meta:
        indexes = [
            models.Index(fields=['business']),
            models.Index(fields=['last_message_at'])
        ]

class AgentAssignment(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    agent = models.ForeignKey("account.User", on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")

class Message(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="messages", blank=True, null=True)
    whatsapp_account = models.ForeignKey('integration.WhatsAppAccount', on_delete=models.SET_NULL, related_name="messages", blank=True, null=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    direction = models.CharField(max_length=20, choices=MESSAGE_DIRECTION.choices)
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPE.choices, default=MESSAGE_TYPE.TEXT)

    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='messages/', null=True, blank=True)

    meta_message_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=MESSAGE_STATUS.choices, default=MESSAGE_STATUS.SENT)
    error_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['meta_message_id']),
            models.Index(fields=['conversation', 'timestamp']),
            models.Index(fields=['business', 'timestamp']),
            models.Index(fields=['lead']),
        ]

class MediaFile(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=50)
    file = models.FileField(upload_to="media/")
    meta_media_id = models.CharField(max_length=255)


class Tag(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

class ConversationTag(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
