from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from core.utils import UpdateModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
from core.choice_select import APP_TITLE, ACTIVITY_LOG_ACTION_TYPE
from .service import ConnectedAppWithToken
from django.db import transaction
from core.utils import UpdateReadOnlyModelViewSet
from notify.service import LogActivityModule


class AppViewSet(UpdateModelViewSet):
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    queryset = App.objects.all()

    @action(detail=True, methods=["get", "post"], url_path="connect")
    def app_connect(self, request, *args, **kwargs):
        app_object = self.get_object()
        user = request.user
        business = user.business.first()
        if business.whatsapp_account.first():
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
                        self.create_log(
                            ACTIVITY_LOG_ACTION_TYPE.CONNECTED, business=business, entity=waba_app
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
    
    # self.create_log("Request Cancel", entity=order, for_notify=True, user=order_request.provider.user, metadata={"reference_user_id": self.request.user.id, "reference_object_id": order_request.id, "reference_object_type": "OrderRequest"})
    def create_log(self, action, business=None, entity=None, for_notify=False, user=None, metadata={}):
        data = {
            "user": user or self.request.user,
            "business": business,
            "action": action,
            "entity": entity,
            "request": self.request,
            "for_notify": for_notify,
            "metadata": metadata,
        }
        log = LogActivityModule(data)
        log.create()
    

class WhatsAppAccountViewSet(ModelViewSet):
    serializer_class = WhatsAppAccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = WhatsAppAccount.objects.all()

    def get_business(self):
        user = self.request.user
        business = user.business.first()
        return business
    
    def get_queryset(self):
        business = self.get_business()
        return WhatsAppAccount.objects.filter(business=business)
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                {
                    'success': True,
                    'data': response.data
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'messgae': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.perform_retrieve(serializer)
    
    def perform_retrieve(self, serializer):
        return Response(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], url_path="discounnect")
    def get_discounnect(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                whatsapp_account = self.get_object()
                self.create_log(
                    ACTIVITY_LOG_ACTION_TYPE.DISCONNECTED, business=whatsapp_account.business, entity=whatsapp_account
                )
                return Response(
                    {
                        "success": True,
                        "message": "Discounnected your whatsapp account!"
                    }, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

    # self.create_log("Request Cancel", entity=order, for_notify=True, user=order_request.provider.user, metadata={"reference_user_id": self.request.user.id, "reference_object_id": order_request.id, "reference_object_type": "OrderRequest"})
    def create_log(self, action, business=None, entity=None, for_notify=False, user=None, metadata={}):
        data = {
            "user": user or self.request.user,
            "business": business,
            "action": action,
            "entity": entity,
            "request": self.request,
            "for_notify": for_notify,
            "metadata": metadata,
        }
        log = LogActivityModule(data)
        log.create()


