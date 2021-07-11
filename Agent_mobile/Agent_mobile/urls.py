from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('Agent_mobile.apps.main_menu.urls')),
    path('index/', include('Agent_mobile.apps.main_menu.urls')),
    path('visit/', include('Agent_mobile.apps.visits.urls')),
    path('invoice/', include('Agent_mobile.apps.invoices.urls')),
    path('items/', include('Agent_mobile.apps.core.urls')),
    path('api/', include('Agent_mobile.api.urls')),
]
