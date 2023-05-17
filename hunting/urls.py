from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads.view.category import root
from hunting import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
    path('cat/', include('ads.urls.category')),
    path('ad/', include('ads.urls.ad')),
    path('user/', include('authentication.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
