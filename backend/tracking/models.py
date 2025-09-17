from django.db import models
from django.contrib.postgres.fields import JSONField  # or models.JSONField on recent Django

class TrackedObject(models.Model):
    camera = models.ForeignKey('cameras.Camera', on_delete=models.SET_NULL, null=True)
    track_id = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=100)       # e.g., "person"
    confidence = models.FloatField(null=True, blank=True)
    bbox = models.JSONField()                       # {x,y,w,h} أو normalized coords
    timestamp = models.DateTimeField()
    frame_number = models.IntegerField(null=True, blank=True)
    extra = models.JSONField(null=True, blank=True)  # أي بيانات إضافية (reid, attributes)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} #{self.track_id} @ {self.camera}"


# Create your models here.
from django.db import models
