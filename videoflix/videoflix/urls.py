
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

#from content.views import VideoViewSet
from content.views import VideoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', VideoViewSet)


if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('django-rq/', include('django_rq.urls')),
    #path('video/', views.VideoViewSet.as_view(), name='video_view'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
