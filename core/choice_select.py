from django.db import models

# Account & Business App-------------------------------
class USER_TYPE(models.TextChoices):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"

class ROLE_TYPE(models.TextChoices):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    AGENT = "AGENT"

class PROFILE_STATUS(models.TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

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



# Integration App-------------------------------
class APP_TITLE(models.TextChoices):
    WHATSAPP_CLOUD = "WHATSAPP_CLOUD"
    MESSANGER = "MESSANGER"


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

class SEND_BY(models.TextChoices):
    AI = "AI"
    AGENT = "AGENT"
    CLIENT = "CLIENT"
    

# class MEDIA_TYPE(models.TextChoices):
#     PDF = "PDF"
#     IMAGE = "Image"
#     AUDIO = "Audio"
#     VIDEO = "Video"

class MESSAGE_STATUS(models.TextChoices):
    SENT = "Sent"
    RECEIVED = "Received"
    DELIVERED = "Delivered"
    READ = "Read"
    FAILED = "Failed"


# Notify App-------------------------------
class ACTIVITY_LOG_ACTION_TYPE(models.TextChoices):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    LOGIN = "Login"
    LOGOUT = "Logout"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"

class WEBHOOK_ACTION(models.TextChoices):
    MESSAGE = "MESSAGE"
    STATUS = "STATUS"

class NOTIFICATION_TYPE(models.TextChoices):
    NEW_MESSAGE = "New_Message"
    SYSTEM = "System_Alert"
    BILLING = "Billing"


# Core App-------------------------------
class AI_MODEL(models.TextChoices):
    OPENAPI = "OPENAPI"
    GEMINI = "GEMINI"


