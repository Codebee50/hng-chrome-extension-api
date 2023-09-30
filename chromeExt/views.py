from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VideoSerialier
from .models import Video
import os
import uuid
from transcribe.views import transcribe, TranscriptionThread
from django.core.files import File


# Create your views here.

class UploadVideo(generics.GenericAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        deferred = request.data.get('deferred')

        if serializer.is_valid():
            video_file = serializer.validated_data.get('video_file')
            new_uuid = str(uuid.uuid4())#generating a uuid to be used as the video name 

            video_name = video_file.name
            file_extension = video_name.split('.')[-1]#getting the file extension of the video

            new_file_name = f'{new_uuid}.{file_extension}'


            if deferred == 'true':
                video_ref = File(video_file, name=new_file_name)
                video_ref.open()
                serializer.save()
                TranscriptionThread(videoFile= video_ref, modelId=serializer.validated_data.get('id')).start()
            else:
                video_file.name = new_file_name#changing the name of the original video file

                transcript = transcribe(videoFile=video_file, deferred=False, modelId=None)
                serializer.save(transcript=transcript)


            return Response({
                'message': 'Video created succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Data is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class VideoDetail(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field = 'pk'
