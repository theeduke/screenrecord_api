# screencast_app/tasks.py
from celery import shared_task
from whisper import transcribe

@shared_task
def transcribe_video(video_path):
    # Use Whisper to transcribe the video
    transcript = transcribe(video_path)
    return transcript
