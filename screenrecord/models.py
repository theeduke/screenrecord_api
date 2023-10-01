from django.db import models

# Create your models here.
class screenRecording(models.Model):
    video = models.FileField(upload_to='screenrecordings/')
    transcript = models.TextField(blank=True, null=True)