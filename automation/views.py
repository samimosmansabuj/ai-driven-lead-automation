from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class AutomationRuleViewSet(ModelViewSet):
    serializer_class = AutomationRuleSerializer
    queryset = AutomationRule.objects.all()


