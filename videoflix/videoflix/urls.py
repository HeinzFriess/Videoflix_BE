from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('django-rq/', include('django_rq.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
