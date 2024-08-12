# EyeOnU

## Testing instructions

1. Install and start [Docker](https://www.docker.com/)
2. [Optional] Install the [Flet App](https://play.google.com/store/apps/details?id=com.appveyor.flet&pli=1) to a mobile device
2. Start the system and demo video stream, execute `docker compose up --build -d`
3. [Optional] Visualize the demo video stream `rtsp://localhost:8554/live.stream` to follow the faces/objects being recognized in real time. You can use [VLC](https://www.videolan.org/vlc/), [`ffplay`](https://ffmpeg.org/ffplay.html), or any video player which supports [RTSP](https://en.wikipedia.org/wiki/Real-Time_Streaming_Protocol)
4. Try the app:
   1. Web: Go to [`http://localhost:8551/app/main.py/`](http://localhost:8551/app/main.py/) in a browser
   1. Mobile: Add the URL `http://<your PC IP>:8551/app/main.py/` as a project in the Flet App
5. The faces and alerts from the demo video stream should appear in the UI, similar to https://youtu.be/APi3yGsOIsY
6. To shutdown execute `docker compose down`