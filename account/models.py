from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel
from core.choice_select import USER_TYPE, PROFILE_STATUS, PROFILE_TYPE

class User(AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE, null=True, blank=True, related_name="user_profile")

    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE.choices)
    language = models.CharField(max_length=20, default='en')
    live_chat_notification_sound = models.BooleanField(default=True)

    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=PROFILE_STATUS.choices, default=PROFILE_STATUS.ACTIVE)
    last_seen = models.DateTimeField(null=True, blank=True)
