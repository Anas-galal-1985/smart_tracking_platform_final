from django.db import models

# Create your models here.

class Camera(models.Model):
    SOURCE_CHOICES = [
        ('rtsp','RTSP'),
        ('file','Video File'),
        ('stream','HTTP Stream'),
    ]
    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    source_url = models.TextField()
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
