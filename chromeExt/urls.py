from django.urls import path
from . import views

urlpatterns =[
    path('video/', views.UploadVideo.as_view(), name='uploadVideo')
]