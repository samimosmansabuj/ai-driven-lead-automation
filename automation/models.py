from django.db import models
from core.models import BaseModel

class AutomationRule(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="automation_rules", null=True, blank=True)
    name = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=50)
    trigger_value = models.CharField(max_length=255)
    response_type = models.CharField(max_length=50)
    response_content = models.JSONField()
    is_active = models.BooleanField(default=True)

class MessageQueue(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="message_queue", null=True, blank=True)
    whatsapp_account = models.ForeignKey('integration.WhatsAppAccount', on_delete=models.SET_NULL, related_name="message_queue", blank=True, null=True)
    payload = models.JSONField()
    status = models.CharField(max_length=20, default='pending')
    retry_count = models.IntegerField(default=0)

