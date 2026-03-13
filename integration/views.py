from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from core.utils import UpdateModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
from core.choice_select import APP_TITLE
from .service import ConnectedAppWithToken
from django.db import transaction


class AppViewSet(UpdateModelViewSet):
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    queryset = App.objects.all()

    @action(detail=True, methods=["get", "post"], url_path="connect")
    def app_connect(self, request, *args, **kwargs):
        app_object = self.get_object()
        user = request.user
        business = user.business.first()
        if business.whatsapp_account:
            return Response(
                {
                    "success": False,
                    "message": "Already whatsapp connect. remove old account first!"
                }
            )
        
        if request.method == "GET":
            if app_object.app_title == APP_TITLE.WHATSAPP_CLOUD:
                redirect_url = app_object.config.get("redirect_url")
                scope = app_object.config.get("scope")
                oauth_url = (
                    "https://www.facebook.com/v23.0/dialog/oauth?"
                    + urllib.parse.urlencode({
                        "client_id": app_object.app_id,
                        "redirect_uri": redirect_url,
                        "scope": scope,
                        # "response_type": "token"
                        "response_type": "code"
                    })
                )
            return Response(
                {
                    "success": True,
                    "oauth_url": oauth_url
                }
            )
        
        if request.method == "POST":
            data = request.POST
            try:
                with transaction.atomic():
                    token_type = request.POST.get("token_type")
                    token = request.POST.get("code")
                    connect_app = ConnectedAppWithToken(token_type, token, app_object)
                    connect_response = connect_app.get_connect()

                    if connect_response.get("status") == "connected":
                        if connect_response.get("waba_name"):
                            business.name = connect_response.get("waba_name")
                        business.meta_business_id = connect_response.get("business_id")
                        business.save(update_fields=['meta_business_id', 'name'])

                        waba_app = WhatsAppAccount.objects.create(
                            business=business,
                            meta_business_id=connect_response.get("business_id"),
                            waba_id=connect_response.get("waba_id"),
                            phone_number_id=connect_response.get("phone_number_id"),
                            display_phone_number=connect_response.get("phones"),
                            access_token=connect_response.get("access_token_json", {})
                        )
                    return Response(
                        {
                            "success": True,
                            "message": "Connected!",
                            "data": connect_response
                        }, status=status.HTTP_200_OK
                    )
            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "message": str(e)
                    }, status=status.HTTP_400_BAD_REQUEST
                )
    

class WhatsAppAccountViewSet(ModelViewSet):
    serializer_class = WhatsAppAccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = WhatsAppAccount.objects.all()

