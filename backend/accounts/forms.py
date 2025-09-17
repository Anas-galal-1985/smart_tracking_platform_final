# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'role', 'avatar']  # أضفنا avatar هنا

from .models import SiteSettings

from django import forms
from .models import SiteSettings

import json
from django import forms
from .models import SiteSettings



class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'navbar_color': forms.Select(attrs={'class': 'form-select'}),
            'cameras_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'advanced_tracking_options': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'maintenance_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
