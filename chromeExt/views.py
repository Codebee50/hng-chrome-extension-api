from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VideoSerialier
from .models import Video
import os
import uuid
from transcribe.views import transcribe, TranscriptionThread
from django.core.files import File
from django.conf import settings
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist


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

            video_file.name = new_file_name#changing the name of the original video file

            if deferred == 'true':
                serializer.save()
                video_path = 'media/videos/' + new_file_name

                video_file_path = os.path.join(settings.BASE_DIR, video_path)
                
                TranscriptionThread(videoFile= None, modelId=serializer.data.get('id'), video_file_path=video_file_path, video_name=new_file_name).start()
            else:

                transcript = transcribe(videoFile=video_file, deferred=False, modelId=None, video_file_path=None, video_name=new_file_name)
                serializer.save(transcript=transcript)


            return Response({
                'message': 'Video created succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            print('the type is ', type(serializer.errors))
            error_message = next(iter(serializer.errors.values()))[0]

            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class VideoDetail(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field = 'pk'


class generateVideoTranscript(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field= 'pk'
    
 
    def get(self, request, *args, **kwargs):
        modelId = kwargs.get('pk')
        try:
            video_model = Video.objects.get(id=modelId)
        except ObjectDoesNotExist:
            return Response({'message': f'A video with an id {modelId} does not exist'}, status= status.HTTP_400_BAD_REQUEST)

        if video_model.transcript == 'pending':#we only want to generate a transcript if the transcript has not been generated before 
            video_path = 'media/' + video_model.video_file.name

            video_file_path = os.path.join(settings.BASE_DIR, video_path)
            video_name = video_model.video_file.name
            parts = video_name.split('/')
            transcribe(videoFile=video_model.video_file, deferred=True, modelId=modelId, video_file_path=video_file_path, video_name=parts[-1])

        return super().get(request, *args, **kwargs)
