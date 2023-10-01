from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VideoSerialier
from .models import Video, VideoSession
import os
import uuid
from transcribe.views import transcribe, TranscriptionThread
from django.core.files import File
from django.conf import settings
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.contrib.sites.shortcuts import get_current_site
import io
import base64
from django.core.files.base import ContentFile



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

@api_view(['POST', 'GET'])
def startVideoSession(reqeust,*args, **kwargs):
    session_uuid = str(uuid.uuid4())#generating a uuid to be used as the video name 
    video_session = VideoSession.objects.create(session_id = session_uuid)

    video_session.save()
    return Response({
        'message': 'Session started succesfully',
        'session_id': session_uuid
    }, status= status.HTTP_201_CREATED)

@api_view(['POST'])
def uploadSessionChunk(request, *args, **kwargs):
    session_id = kwargs.get('session_id')
    try:
        video_session = VideoSession.objects.get(session_id = session_id)
    except ObjectDoesNotExist:
        video_session = None


    if video_session is not None:
        video_chunk = request.FILES.get('video_chunk')
        print(type(video_chunk))

        binary_data = bytes(video_chunk.read())
        
        if video_session.chunks is not None:
            video_chunk_list = [video_session.chunks, binary_data]
            video_buffer = b''.join(chunk for chunk in video_chunk_list)
            video_session.chunks = video_buffer
        else:
            video_session.chunks = binary_data

        video_session.save()

        return Response({
            'message': 'chunk added succesfully'
        }, status= status.HTTP_201_CREATED)
    else:
        return Response({
            'message': 'invalid session id'
        }, status= status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def uploadSessionChunkArray(request, *args, **kwargs):
    session_id = kwargs.get('session_id')
    # received_data = request.POST.getlist('blobs[]')

    try:
        video_session = VideoSession.objects.get(session_id = session_id)
    except ObjectDoesNotExist:
        return Response({'message': 'Video session not found'})

    chunk_array = request.data.get('chunk_array')
    for blob_chunk in chunk_array:
        print(type(blob_chunk))
        video_chunk = ContentFile(base64.b64decode(blob_chunk))

        print(type(video_chunk))
        binary_data = bytes(video_chunk.read())
        
        if video_session.chunks is not None:
            video_chunk_list = [video_session.chunks, binary_data]
            video_buffer = b''.join(chunk for chunk in video_chunk_list)
            video_session.chunks = video_buffer
        else:
            video_session.chunks = binary_data

        video_session.save()

    return Response({
        'message': 'Chunk array uploaded succesfully'
    }, status= status.HTTP_201_CREATED)



class completeVideoSession(generics.GenericAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        deferred = request.data.get('deferred')

        try:
            video_session = VideoSession.objects.get(session_id=session_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Video session not found'}, status=status.HTTP_404_NOT_FOUND)

        binary_data = video_session.chunks

        
        file_object = io.BytesIO(binary_data)#creating a file object out of the binary data in the video session chunks
        file = File(file_object)
        file.name = 'recorded.webm'
        data = {
            'video_title': request.data.get('video_title'),
            'deferred': request.data.get('deferred'),
            'video_file': file,
        }
        serializer = self.get_serializer(data=data)

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

            video_session.delete()
            return Response({
                'message': 'Video created succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            error_message = next(iter(serializer.errors.values()))[0]
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

   
@api_view(['POST'])
def cancelVideoSession(request, *args, **kwargs):
    session_id = kwargs.get('session_id')
    
    try:
        video_session = VideoSession.objects.get(session_id=session_id)
    except ObjectDoesNotExist:
        return Response({'message': 'Video session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    video_session.delete()
    return Response('message', 'Session cancelled succesfully', status= status.HTTP_200_OK)

    
