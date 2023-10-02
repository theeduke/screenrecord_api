from django import forms
from .models import screenRecording

class VideoUploadForm(forms.Form):
    class Meta:
        model = screenRecording
        fields = ["video"]