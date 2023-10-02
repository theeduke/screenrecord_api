from celery import Celery

app = Celery('video_player')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()