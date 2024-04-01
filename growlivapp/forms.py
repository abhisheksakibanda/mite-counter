from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Video, Business


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']


class BusinessForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'un', 'placeholder': field.label})

    class Meta:
        model = Business
        fields = ['email', 'password1', 'password2', 'business_name', 'business_phone', 'contact_person_name']
