from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('admin','Admin'),
        ('viewer','Viewer'),
        ('operator','Operator'),
    ], default='viewer')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # صورة البروفايل
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
class SiteSettings(models.Model):
    NAVBAR_COLORS = [
        ('primary', 'Blue'),
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('success', 'Green'),
        ('warning', 'Yellow'),
        ('danger', 'Red'),
    ]
    navbar_color = models.CharField(max_length=20, choices=NAVBAR_COLORS, default='primary')
    cameras_enabled = models.BooleanField(default=True)
    advanced_tracking_options = models.JSONField(default=dict, blank=True)
    site_name = models.CharField(max_length=100, default="Smart Tracking Platform")
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "SiteSettings"

