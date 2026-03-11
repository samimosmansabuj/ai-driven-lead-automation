from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from core.utils import UpdateModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import urllib.parse


class AppViewSet(UpdateModelViewSet):
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    queryset = App.objects.all()

    @action(detail=True, methods=["get"], url_path="connect")
    def app_connect(self, request, *args, **kwargs):
        app_object = self.get_object()

        if app_object.app_title == "whatsapp_cloud":
            redirect_url = app_object.config.get("redirect_url")
            scope = app_object.config.get("scope")
            oauth_url = (
                "https://www.facebook.com/v23.0/dialog/oauth?"
                + urllib.parse.urlencode({
                    "client_id": app_object.app_id,
                    "redirect_uri": redirect_url,
                    "scope": scope,
                    "response_type": "code"
                })
            )
        return Response(
            {
                "success": True,
                "oauth_url": oauth_url
            }
        )
        
    




class WhatsAppAccountViewSet(ModelViewSet):
    serializer_class = WhatsAppAccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = WhatsAppAccount.objects.all()