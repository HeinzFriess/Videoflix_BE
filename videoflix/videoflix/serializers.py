from rest_framework import serializers

from content.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'  # You can specify specific fields if needed
