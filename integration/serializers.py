from rest_framework import serializers
from .models import *


class WhatsAppAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppAccount
        fields = "__all__"


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"

