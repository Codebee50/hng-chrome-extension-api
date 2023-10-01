# HNG stage five
## Chrome extension api documentation

## Getting started 
online api domain => https://codebee.pythonanywhere.com

# POST -> Start a new session
This creates a new video session and returns the session_id, which can be used to upload video chunks to that session 
```
http://codebee.pythonanywhere.com/api/start-session/
```
### Returns
`{
        'message': 'Session started succesfully',
        'session_id': 87a9bb00-e605-4f61-988d-717c92832a51
    }`
    and a status code of 201 if session was started succesfully

# POST -> Upload a chunk 
This appends a video chunk to the session specified by the session_id


```
http://codebee.pythonanywhere.com/api/upload-chunk/:session_id/
```

### Body
```json
{
    "video_chunk": "<chunk>"
}
```
chunk should be in blob format

# POST -> Complete session
This endpoint assumes that recordinig is complete, concatenates all the chunks in the session and saves as a video file. The deferred variable in the reqeust body indicates that trancription shouldnt be done now but left for later, as transcription might cause long waiting periods

```
https://codebee.pythonanywhere.com/api/complete-session/:session_id/
```

### Body
```json
{
    "video_title" : "<A title for the recording>",
    "deferred" : "true"
}

```

### Returns
```json
{
    "message": "Video created succesfully",
    "data": {
        "video_title": "A test for online",
        "created_at": "2023-10-01T16:11:05.102558Z",
        "date_created": "2023-10-01",
        "time_created": "16:11:05",
        "video_file": "https://codebee.pythonanywhere.com/media/videos/76603429-282f-40d2-9832-3c32ecc4d2be.webm",
        "transcript": "pending",
        "id": 8
    }
}
```
with a status code of 201 if video was created succesfully

```json
{
    "message": "<Appropriate error message>"
}
```
with as status code of 400 if an error occurs 




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
the `deferred` attribute specifies if transcript should be generated while creating the video. if `deferred` is false, the transcript for the video is generated instantly but this might take some time for long videos hence causing long waiting periods. When true, the transcript is not generated and is set to pending a transcript can be genreated later on using the `transcribe-video` endpoint, this is done to improve speed for create video requests. 


### Returns 
```json
{
    "message": "A video with the title (A sample title changed) already exists"
}

```
with a status code of `400` if video title already exists


```json
{
    "message": "Video created succesfully",
    "data": {
        "video_title": "A sample",
        "created_at": "2023-09-30T20:20:23.703069Z",
        "date_created": "2023-09-30",
        "time_created": "20:20:23",
        "video_file": "http://codebee.pythonanywhere.com/media/videos/e3023fe2-dc13-4c10-bf54-3e42d1e8d92f.mp4",
        "transcript": "pending",
        "id": 93
    }
}

```
with a status code of `201` if `deferred` was set to `true` and video was created succesfully

```json

{
    "message": "Video created succesfully",
    "data": {
        "video_title": "A sample video",
        "created_at": "2023-09-30T20:24:11.863986Z",
        "date_created": "2023-09-30",
        "time_created": "20:24:11",
        "video_file": "http://codebee.pythonanywhere.com/media/videos/5d82c55d-3ab1-4320-907e-5768ad51e576.mp4",
        "transcript": "transcript of the video goes here",
        "id": 94
    }
}
```
with a status code of `201` if `deferred` was set to `false` and video was created succesfully

# GET -> Get a video

```
https://codebee.pythonanywhere.com/api/video/:id/
```
### Path variables
* id -> the id of the video to be retrieved

### Returns
```json

{
    "video_title": "A sample video title",
    "created_at": "2023-09-30T16:46:48.666902Z",
    "date_created": "2023-09-30",
    "time_created": "16:46:48",
    "video_file": "http://codebee.pythonanywhere.com/media/videos/f8f716cf-4cbd-4725-bb64-6463077586eb.mp4",
    "transcript": "A sample video transcript",
    "id": 4
}

```


# GET -> Get all videos
``````
https://codebee.pythonanywhere.com/api/video/
 
``````

# Returns

```
[
    A list of all videos in the database
]
```

# GET -> Transcribe a video 

```
https://codebee.pythonanywhere.com/api/transcribe-video/:id/

```
This endpoint is used to get the transcription of videos whose transcript were previously pending 

### Path variables
* id -> the id of the video to be transcribed

### Returns
``` json
{
    "video_title": "Video of someone jumping to get fila shoes",
    "created_at": "2023-09-30T20:38:05.326343Z",
    "date_created": "2023-09-30",
    "time_created": "20:38:05",
    "video_file": "https://codebee.pythonanywhere.com/media/videos/f8f716cf-4cbd-4725-bb64-6463077586eb.mp4",
    "transcript": "if you're able to make this jump you get free Fila shoes and this guy was about to make his attempt but little did anyone know he's secretly a hurdler",
    "id": 4
}

```
with a status of 200 







