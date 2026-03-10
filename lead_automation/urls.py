from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('api/v1/', include("account.urls")),
    path('api/v1/', include("automation.urls")),
    path('api/v1/', include("billing.urls")),
    path('api/v1/', include("business.urls")),
    path('api/v1/', include("core.urls")),
    path('api/v1/', include("integration.urls")),
    path('api/v1/', include("lead.urls")),
    path('api/v1/', include("notify.urls")),
]
