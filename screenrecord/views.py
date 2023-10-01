from django.shortcuts import render, get_object_or_404, redirect
from django.http import StreamingHttpResponse, JsonResponse
from .models import screenRecording
import os
from .forms import VideoUploadForm
from .tasks import transcribe_video
from celery.result import AsyncResult
# Create your views here.

def receive_screen_recording(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']
            video_name = video.name
            video_path = os.path.join('uploads', video_name)
            
            #save the video to 'uploads' directory
            with open(video_path,  'wb') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
                    
            #redirect to video playback page
            return redirect('playback', video_name=video_name)
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

def playback(request, video_name):
    video_path = os.path.join('uploads', video_name)
    
    # Check if transcription task is complete
    recording = screenRecording.objects.filter(video=video_path).first()
    if recording and recording.transcription_task_id:
        result = AsyncResult(recording.transcription_task_id)
        if result.successful():
            transcript = result.result
            # Handle the transcript, e.g., save to database, display to user
            return render(request, 'playback.html', {'recording': recording, 'transcript': transcript})
        elif result.failed():
            error_message = str(result.result)
            return JsonResponse({'error': error_message})
        else:
            return JsonResponse({'status': 'in_progress'})
    else:
        return JsonResponse({'error': 'Transcription not yet initiated.'})