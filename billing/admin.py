from django.contrib import admin
from .models import (
    SubscriptionPlan,
    SubscriptionPlanFeature,
    BusinessSubscription,
    Invoice
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "unit", "price", "message_limit", "agent_limit", "status")
    list_filter = ("status", "unit")
    search_fields = ("title",)


@admin.register(SubscriptionPlanFeature)
class SubscriptionPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("id", "plan", "name", "value", "status")
    list_filter = ("status",)


@admin.register(BusinessSubscription)
class BusinessSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "plan", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "business", "amount", "currency", "status", "paid_at")
    search_fields = ("invoice_number",)
    list_filter = ("status",)