# HNG stage five
## Chrome extension api documentation

## Getting started 
online api domain => http://codebee.pythonanywhere.com

# POST -> Create a new video
``````
https://codebee.pythonanywhere.com/api/video/
 
 ``````

### Body 
```json
{
    "video_title": "A title",
    "video_file" :  "<the video file to be uploaded>",
    "deferred": "false"
}
```
the `defered` attribute specifies if transcript should be generated while creating the video if it is false, the transcript for the video is generated instantly but this might take some time for long videos hence causing waiting periods. When true, the transcript is not generated and is set to pending a transcript can be genreated later on using the `transcribe-video` endpoint, this is done to improve speed of creating videos. 


