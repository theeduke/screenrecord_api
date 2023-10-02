from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import screenRecording
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import VideoUploadForm
from .tasks import transcribe_video
from celery.result import AsyncResult
# Create your views here.
@api_view(['POST'])
def receive_screen_recording(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']
            video_name = video.name
            video_path = os.path.join('media','uploads', video_name)
            
            #save the video to 'uploads' directory
            with open(video_path,  'wb') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
                    
            #redirect to video playback page
            return Response({'video_name': video_name}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def playback(request, video_name):
    video_path = os.path.join('media','uploads', video_name)
    
    # Check if transcription task is complete
    recording = screenRecording.objects.filter(video=video_path).first()
    if recording and recording.transcription_task_id:
        result = AsyncResult(recording.transcription_task_id)
        if result.successful():
            transcript = result.result
            # Handle the transcript, save to database, display to user
            try:
                with open(transcript, 'rb') as transcript:
                    response = StreamingHttpResponse(transcript, content_type='video/mp4')
                    response['Content-Disposition'] = f'inline; filename="{video_name}"'
                    return response
            except FileNotFoundError:
                return JsonResponse({'error': 'Transcribed video not found'}, status=404)
        elif result.failed():
            error_message = str(result.result)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': 'in_progress'}, status=status.HTTP_200_OK)
    else:
        task_result = transcribe_video.delay(video_path)
        recording.transcription_task_id = task_result.id
        recording.save()
        
        return Response({'status': 'transcription_initiated'}, status=status.HTTP_200_OK)
    