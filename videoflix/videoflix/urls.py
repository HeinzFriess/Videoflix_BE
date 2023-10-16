
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from content.views import VideoViewSet
from users.views import adduserview, signupview, loginview

router = DefaultRouter()
router.register(r'videos', VideoViewSet)


if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('login/', loginview.as_view()),
    path('signup/', signupview.as_view()),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('django-rq/', include('django_rq.urls')),
    path('adduser/', adduserview.as_view()),
    #path('video/', views.VideoViewSet.as_view(), name='video_view'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
