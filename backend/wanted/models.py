# wanted/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField  # إذا كنت تستخدم PostgreSQL
from tracking.models import TrackedObject

class WantedPerson(models.Model):
    tracked_object = models.OneToOneField(
        TrackedObject,
        on_delete=models.CASCADE,
        related_name="wanted_person",
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="wanted_photos/")
    found = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    face_embedding = ArrayField(models.FloatField(), null=True, blank=True)  # <--- بصمة الوجه
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
