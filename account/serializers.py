from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.choice_select import USER_TYPE, ROLE_TYPE
from business.models import Business, BusinessMember
from django.db import transaction

# =================================================================
# Business Client/Member Login Start===========================
class LoginTokenSerializer(TokenObtainPairSerializer):
    def get_user(self):
        if self.user.user_type != USER_TYPE.CLIENT:
            raise Exception("Only client user can login!")
        return self.user

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    business_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["id", "business_name", "email", "password", "confirm_password"]
    
    def create_business(self, user, business_name):
        return Business.objects.create(
            owner=user,
            name=business_name
        )
    
    def check_password(self, password, confirm_password):
        if password != confirm_password:
            raise Exception("Password and confirm password is not same!")

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop("password")
            confirm_password = validated_data.pop("confirm_password")
            self.check_password(password, confirm_password)

            business_name = validated_data.pop("business_name")

            user = User.objects.create(**validated_data)
            user.username = user.email
            user.set_password(password)
            user.save()

            business = self.create_business(user, business_name)
            BusinessMember.objects.create(user=user, business=business, role=ROLE_TYPE.ADMIN)
            return user

class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = BusinessMember
        fields = ["id", "name", "username", "email", "role", "language", "live_chat_notification_sound", "profile_picture", "status"]

# Business Client/Member Login End===========================
# =================================================================




