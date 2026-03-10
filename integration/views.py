from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class WhatsAppAccountViewSet(ModelViewSet):
    serializer_class = WhatsAppAccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = WhatsAppAccount.objects.all()