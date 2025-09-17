from django.contrib import admin
from .models import Camera

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'source_type', 'location', 'created_at')
    search_fields = ('name', 'source_url', 'location')
    list_filter = ('is_active', 'source_type', 'created_at')
