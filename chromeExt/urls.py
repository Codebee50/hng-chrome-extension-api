from django.urls import path
from . import views

urlpatterns =[
    path('video/', views.UploadVideo.as_view(), name='upload-video'),
    path('video/<str:pk>/', views.VideoDetail.as_view(), name='product-detail'),
    path('delete-video/<str:pk>/', views.DestroyVideo.as_view(), name='deletevideo'),
    path('transcribe-video/<str:pk>/', views.generateVideoTranscript.as_view(), name='generate-transcription'),
    path('start-session/', views.startVideoSession, name='startvideosession'),
    path('upload-chunk/<str:session_id>/', views.uploadSessionChunk, name='uploadsessionchunk'),
    path('complete-session/<str:session_id>/', views.completeVideoSession.as_view(), name='completesession'),
    path('cancel-session/<str:session_id>/', views.cancelVideoSession, name='cancelvideosession'),
    path('upload-chunk-array/<str:session_id>/', views.uploadSessionChunkArray, name='uploadchunkarray')
]