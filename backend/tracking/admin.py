from django.contrib import admin
from .models import TrackedObject

@admin.register(TrackedObject)
class TrackedObjectAdmin(admin.ModelAdmin):
    list_display = ('label', 'track_id', 'camera', 'timestamp', 'frame_number')
    search_fields = ('label', 'track_id', 'camera__name')
    list_filter = ('camera', 'timestamp', 'label')
