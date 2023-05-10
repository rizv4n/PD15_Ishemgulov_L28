from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import LocationsViewSet

from ads.view.category import root
from hunting import settings

router = routers.SimpleRouter()
router.register('location', LocationsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
    path('cat/', include('ads.urls.category')),
    path('ad/', include('ads.urls.ad')),
    path('user/', include('users.url'))
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
