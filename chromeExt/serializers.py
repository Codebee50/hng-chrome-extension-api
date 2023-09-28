from rest_framework import serializers
from .models import Video

class VideoSerialier(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = [
            'video_title',
            'id',
        ]