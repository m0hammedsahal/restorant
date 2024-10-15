
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from manager import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ("web.urls", namespace="web")),
    path('manager/', include ("manager.urls", namespace="manager")),
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

