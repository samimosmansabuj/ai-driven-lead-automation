from django.contrib import admin
from django.urls import path
from .views import HomePage, ConnectWhatsapp, WebhookWhatsapp, WhatsappCallbackView, PrivacyPolicyView, WebhookWhatsappTest, SendMessageView

urlpatterns = [
    path("", HomePage.as_view(), name="HomePage"),
    path("webhook/whatsapp/", WebhookWhatsapp.as_view(), name="WebhookWhatsapp"),
    path("webhook/whatsapp/test/", WebhookWhatsappTest.as_view(), name="WebhookWhatsapp"),

    path("callback/whatsapp/", WhatsappCallbackView.as_view(), name="WhatsappCallbackView"),
    path("connect-whatsapp/", ConnectWhatsapp.as_view(), name="ConnectWhatsapp"),
    path("send-message/", SendMessageView.as_view(), name="SendMessageView"),

    
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="PrivacyPolicyView"),
]