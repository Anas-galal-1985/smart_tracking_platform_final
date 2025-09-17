from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=100)
    rtsp_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class VideoStream(models.Model):
    title = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to='videos/', blank=True, null=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, blank=True, null=True)
    is_live = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #person_count = models.IntegerField(default=0)  # عدد الأشخاص المكتشفين حالياً

    def __str__(self):
        return self.title
