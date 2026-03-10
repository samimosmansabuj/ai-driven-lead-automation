from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("business", BusinessViewSet)
router.register("members", BusinessMemberViewSet)



urlpatterns = [
    path("", include(router.urls))
]

# urlpatterns += router.urls
