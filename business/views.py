from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from core.utils import UpdateModelViewSet


class BusinessViewSet(UpdateModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BusinessMemberViewSet(ModelViewSet):
    serializer_class = BusinessMemberSerializer
    permission_classes = [IsAuthenticated]
    queryset = BusinessMember.objects.all()

