from django import forms
from .models import TrackedObject

class TrackedObjectForm(forms.ModelForm):
    class Meta:
        model = TrackedObject
        fields = ['camera', 'track_id', 'label', 'confidence', 'bbox', 'timestamp', 'frame_number', 'extra']
