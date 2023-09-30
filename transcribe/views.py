from django.shortcuts import render
import speech_recognition as sr
from pydub import AudioSegment
import os
import threading
from chromeExt.models import Video
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.conf import settings




class TranscriptionThread(threading.Thread):
    def __init__(self, videoFile, modelId):
        self.videoFile = videoFile
        self.modelId = modelId
        threading.Thread.__init__(self)
        
    def run(self) -> None:
        transcribe(self.videoFile, True, self.modelId)

# Create your views here.


def transcribe(videoFile, deferred, modelId):
    """
    This function gets the transcription of a video file

    Args:
        :videoFile: the video file to be transcribed
        :deffered: indicates if the transcription should be done now or if it was deffered for later
    """
    if deferred:
        videoFile = File(open(videoFile))
        
    video_name = videoFile.name
    parts = video_name.split('.')#spliting the name of the document into parts base on the '.' symbol
    file_extension = parts[-1]#getting the last item in the list will will be the file extension 

    video = AudioSegment.from_file(videoFile, format=file_extension)
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)


    audio_file_name = f"audio-{video_name}"

    audio_file_path = os.path.join(settings.BASE_DIR, f"audio/{audio_file_name}")

    audio.export(audio_file_path, format="wav")#creating an audio file from the video file in wav format for transcribing

    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_text = r.record(source=source)
    
    text = r.recognize_google(audio_text, language='en-US')
    # os.remove(audio_file_path)

    if deferred: #this means the task of transcribing was left for later, we need to update the model
        try:
            video_model = Video.objects.get(id = modelId)
        except ObjectDoesNotExist:
            video_model = None
        
        if video is not None:
            video_model.transcript = text
            video_model.save()
    else:
        return text