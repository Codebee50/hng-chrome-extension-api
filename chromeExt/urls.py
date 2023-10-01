from django.urls import path
from . import views

urlpatterns =[
    path('video/', views.UploadVideo.as_view(), name='upload-video'),
    path('video/<str:pk>/', views.VideoDetail.as_view(), name='product-detail'),
    path('transcribe-video/<str:pk>/', views.generateVideoTranscript.as_view(), name='generate-transcription'),
    path('start-session/', views.startVideoSession, name='startvideosession'),
    path('upload-chunk/<str:session_id>/', views.uploadSessionChunk, name='uploadsessionchunk'),
    path('complete-session/<str:session_id>/', views.completeSession, name='completesession')
]