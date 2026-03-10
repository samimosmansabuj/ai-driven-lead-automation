from rest_framework import serializers
from .models import *


class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = "__all__"


class MessageQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageQueue
        fields = "__all__"