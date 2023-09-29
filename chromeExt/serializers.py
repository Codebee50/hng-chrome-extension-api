from rest_framework import serializers
from .models import Video
from datetime import datetime

class VideoSerialier(serializers.ModelSerializer):
    time_created = serializers.SerializerMethodField(read_only=True)
    date_created = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Video
        fields = [
            'video_title',
            'created_at',
            'date_created',
            'time_created',
            'video_file',
            'id',
        ]

    def get_date_created(self, obj):
        created_at = getattr(obj,'created_at')
        formatted_date = created_at.strftime('%Y-%m-%d')
        return formatted_date
    
    def get_time_created(self, obj):
        created_at = getattr(obj, 'created_at')
        formatted_time = created_at.strftime('%H:%M:%S')
        return formatted_time        


    