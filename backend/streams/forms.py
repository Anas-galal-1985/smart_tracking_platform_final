# streams/forms.py
from django import forms
from .models import VideoStream, Camera

class VideoStreamForm(forms.ModelForm):
    class Meta:
        model = VideoStream
        fields = ['title', 'uploaded_file', 'is_live', 'camera']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل عنوان الفيديو أو البث'}),
            'uploaded_file': forms.FileInput(attrs={'class': 'form-control'}),
            'camera': forms.Select(attrs={'class': 'form-control'}),
            'is_live': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
