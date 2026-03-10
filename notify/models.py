from django.db import models
from core.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.choice_select import ACTIVITY_LOG_ACTION_TYPE, NOTIFICATION_TYPE

class ActivityLog(BaseModel):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey("business.Business", on_delete=models.SET_NULL, null=True)

    action = models.CharField(max_length=50, choices=ACTIVITY_LOG_ACTION_TYPE.choices)
    entity_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    entity_id = models.PositiveBigIntegerField(blank=True, null=True)
    service = GenericForeignKey('entity_type', 'entity_id')
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    need_notify = models.BooleanField(default=False)

class Notification(BaseModel):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    business = models.ForeignKey("business.Business", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

class WebhookLog(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="webhook_log", null=True, blank=True)
    payload = models.JSONField()
    event_type = models.CharField(max_length=100)
    processed = models.BooleanField(default=False)

class APILog(BaseModel):
    endpoint = models.CharField(max_length=255)
    request_payload = models.JSONField()
    response_payload = models.JSONField()
    status_code = models.IntegerField()

class AIResponseLog(BaseModel):
    business = models.ForeignKey("business.Business", on_delete=models.CASCADE)
    conversation = models.ForeignKey("lead.Conversation", on_delete=models.CASCADE)
    prompt = models.TextField()
    ai_response = models.TextField()
    tokens_used = models.IntegerField()
