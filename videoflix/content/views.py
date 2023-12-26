from django.core.cache.backends.base import DEFAULT_TIMEOUT 
from django.conf import settings
from rest_framework import viewsets
from .models import Video
from videoflix.serializers import VideoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#Für die view : @cachepage(CACHE_TTL)

class VideoViewSet(viewsets.ModelViewSet):
    """
    API Endpoint to the Videos
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

