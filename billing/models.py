from django.db import models
from core.models import BaseModel
from core.choice_select import SUBSCRIPTION_UNIT, PLAN_STATUS, PLAN_FEATURE_STATUS, INVOICE_STATUS

class SubscriptionPlan(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit = models.CharField(max_length=20, choices=SUBSCRIPTION_UNIT.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PLAN_STATUS.choices, default=PLAN_STATUS.ACTIVE)
    message_limit = models.IntegerField(default=1000)
    agent_limit = models.IntegerField(default=1)

class SubscriptionPlanFeature(BaseModel):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="plan_feature")
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PLAN_FEATURE_STATUS.choices, default=PLAN_FEATURE_STATUS.ACTIVE)

class BusinessSubscription(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="subscription", blank=True, null=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, related_name="subscription", blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

class Invoice(BaseModel):
    business = models.ForeignKey('business.Business', on_delete=models.SET_NULL, related_name="invoices", blank=True, null=True)
    subscription = models.ForeignKey(BusinessSubscription, on_delete=models.SET_NULL, related_name="invoices", blank=True, null=True)
    invoice_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=INVOICE_STATUS.choices, default=INVOICE_STATUS.PENDING)
    payment_reference = models.CharField(max_length=255, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)



