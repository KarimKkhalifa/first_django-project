from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('', include('likes.urls')),
    path('', include('user.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
