
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from notify.models import Notification, ActivityLog


class LogActivityModule:
    def get_confirm_data(self, field, field_name):
        if not field:
            raise Exception(f"{field_name} is missing.")
        return field
    
    def __init__(self, data: dict):
        user = data.get("user")
        print("user: ", user)
        if hasattr(user, "user"):
            user = user.user
        self.user = self.get_confirm_data(user, "User")
        self.action = self.get_confirm_data(data.get("action"), "Action")
        self.entity = data.get("entity")
        self.request = self.get_confirm_data(data.get("request"), "Request")
        self.metadata = data.get("metadata", {})
        self.need_notify = data.get("for_notify", False)
    
    def get_entity_type(self):
        if self.entity is None:
            return None
        elif not hasattr(self.entity, "_meta"):
            raise Exception("Entity must be a Django model instance.")
        else:
            return ContentType.objects.get_for_model(self.entity)

    def get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def get_data(self):
        dict_data = {
            "user": self.user,
            "action": self.action,
            "metadata": self.metadata,
            "ip_address": self.get_ip(self.request),
            "need_notify": self.need_notify
        }
        if self.entity:
            dict_data["entity_type"] = self.get_entity_type()
            dict_data["entity_id"] = self.entity.id
        return dict_data

    def create(self):
        try:
            with transaction.atomic():
                log = ActivityLog.objects.create(
                    **self.get_data()
                )
                return log
        except Exception as e:
            print("error: ", e)
            raise Exception("Someting wrong for create log!")