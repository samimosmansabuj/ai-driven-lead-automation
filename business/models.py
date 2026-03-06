from core.models import BaseModel
from core.choice_select import BUSINESS_STATUS, BUSINESS_DAY, TEAM_INVITE_STATUS
from django.db import models
from django.conf import settings

class Business(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='business/logo/', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    meta_business_id = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=BUSINESS_STATUS.choices, default=BUSINESS_STATUS.ACTIVE)
    timezone = models.CharField(max_length=100, default='UTC')

class BusinessHours(BaseModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="business_hour")
    day = models.IntegerField(choices=BUSINESS_DAY.choices)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

class TeamInvite(BaseModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    invited_by = models.ForeignKey("account.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TEAM_INVITE_STATUS.choices, default=TEAM_INVITE_STATUS.PENDING)

