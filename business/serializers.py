from rest_framework import serializers
from .models import *

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = "__all__"

class BusinessMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessMember
        fields = "__all__"