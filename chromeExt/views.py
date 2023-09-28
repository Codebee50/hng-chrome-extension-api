from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import VideoSerialier
from .models import Video

# Create your views here.

class UploadVideo(generics.GenericAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerialier
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            return Response({
                'message': serializer.data
            })
        else:
            return Response({'message': 'serializer is not valid'})
