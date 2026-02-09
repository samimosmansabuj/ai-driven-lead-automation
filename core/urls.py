from django.contrib import admin
from django.urls import path
from .views import HomePage, ConnectWhatsapp, WebhookWhatsapp, WhatsappCallbackView, PrivacyPolicyView

urlpatterns = [
    path("", HomePage.as_view(), name="HomePage"),
    path("webhook/whatsapp/", WebhookWhatsapp.as_view(), name="WebhookWhatsapp"),
    path("callback/whatsapp/", WhatsappCallbackView.as_view(), name="WhatsappCallbackView"),
    path("connect-whatsapp", ConnectWhatsapp.as_view(), name="ConnectWhatsapp"),

    
    path("privacy-policy", PrivacyPolicyView.as_view(), name="PrivacyPolicyView"),
]