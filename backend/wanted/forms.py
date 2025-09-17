from django import forms
from .models import WantedPerson

class WantedPersonForm(forms.ModelForm):
    class Meta:
        model = WantedPerson
        fields = ['tracked_object', 'full_name', 'photo', 'found', 'last_seen']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tracked_object': forms.Select(attrs={'class': 'form-select'}),
            'found': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_seen': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 5*1024*1024:  # 5MB
            raise forms.ValidationError("حجم الصورة أكبر من 5MB")
        return photo
