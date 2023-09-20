#from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT 
#from django.views.decorators.cache import cachepage 
from django.conf import settings

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#Für die view : @cachepage(CACHE_TTL)