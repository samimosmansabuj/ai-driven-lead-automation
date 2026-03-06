from django.db import models

# Account App-------------------------------
class USER_TYPE(models.TextChoices):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"

class PROFILE_TYPE(models.TextChoices):
    ADMIN = "ADMIN"
    AGENT = "AGENT"

class PROFILE_STATUS(models.TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


# Business App-------------------------------
class BUSINESS_STATUS(models.TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class BUSINESS_DAY(models.TextChoices):
    ONE = "Monday"
    TWO = "Tuesday"
    THREE = "Wednesday"
    FOUR = "Thursday"
    FIVE = "Friday"
    SIX = "Saturday"
    SEVEN = "Sunday"

class TEAM_INVITE_STATUS(models.TextChoices):
    PENDING = "Pending"
    ACTIVE = "Active"
    INACTIVE = "Inactive"

# Subscription App-------------------------------
class SUBSCRIPTION_UNIT(models.TextChoices):
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"

class PLAN_STATUS(models.TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class PLAN_FEATURE_STATUS(models.TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class INVOICE_STATUS(models.TextChoices):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECT = "REJECT"
    CANCEL = "CANCEL"


# LEAD App-------------------------------
class CONVERSATION_STATUS(models.TextChoices):
    OPEN = "open"
    CLOSED = "closed"
    EXPIRED = "expired"
    TRANSFERRED = "transferred"

class CONVERSATION_SOURCE(models.TextChoices):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"

class MESSAGE_DIRECTION(models.TextChoices):
    INCOMING = "Incoming"
    OUTGOING = "Outgoing"

class MESSAGE_TYPE(models.TextChoices):
    TEXT = "Text"
    IMAGE = "Image"
    AUDIO = "Audio"
    VIDEO = "Video"
    FILE = "File"

# class MEDIA_TYPE(models.TextChoices):
#     PDF = "PDF"
#     IMAGE = "Image"
#     AUDIO = "Audio"
#     VIDEO = "Video"

class MESSAGE_STATUS(models.TextChoices):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"
    FAILED = "Failed"


# Notify App-------------------------------
class AUDIT_LOG_ACTION_TYPE(models.TextChoices):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    LOGIN = "Login"
    LOGOUT = "Logout"

class NOTIFICATION_TYPE(models.TextChoices):
    NEW_MESSAGE = "New_Message"
    SYSTEM = "System_Alert"
    BILLING = "Billing"
