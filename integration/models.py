from core.models import BaseModel
from django.db import models

class App(BaseModel):
    name = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    webhook_verify_token = models.CharField(max_length=255)
    config = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

class WhatsAppAccount(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE, related_name="whatsapp_account")
    waba_id = models.CharField(max_length=255)
    phone_number_id = models.CharField(max_length=255)
    display_phone_number = models.CharField(max_length=50)

    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    quality_rating = models.CharField(max_length=50, null=True, blank=True)
    messaging_limit_tier = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['phone_number_id']),
            models.Index(fields=['business']),
        ]