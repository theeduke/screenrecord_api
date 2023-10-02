from django.urls import path
from .views import receive_screen_recording, playback
urlpatterns = [
    path('receive/', receive_screen_recording, name='receive'),
    path('playback/<str:video_name>/', playback, name='playback'),
]