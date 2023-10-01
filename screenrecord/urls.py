from django.urls import path
from .views import receive_screen_recording, playback
urlpatterns = [
    path('receive/', receive_screen_recording, name='receive'),
    path('playback/<int:pk>/', playback, name='playback'),
]