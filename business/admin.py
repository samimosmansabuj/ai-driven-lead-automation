from django.contrib import admin
from .models import Business, BusinessHours, BusinessMember


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "is_verified", "created_at")
    list_filter = ("status", "is_verified")
    search_fields = ("name",)


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "day", "open_time", "close_time", "is_closed")
    list_filter = ("day", "is_closed")


@admin.register(BusinessMember)
class BusinessMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "user__email", "role", "status")
    search_fields = ("user__email",)
    list_filter = ("role", "status")