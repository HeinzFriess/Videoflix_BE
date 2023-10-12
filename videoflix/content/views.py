#from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT 
#from django.views.decorators.cache import cachepage 
from django.conf import settings

from rest_framework import viewsets
from content.models import Video
from videoflix.serializers import VideoSerializer

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#Für die view : @cachepage(CACHE_TTL)

class VideoViewSet(viewsets.ModelViewSet):
    """
    API Endpoint to the Videos
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer