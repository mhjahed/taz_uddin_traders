# core/forms.py
from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image', 'position', 'link_url', 'order', 'is_active']
        widgets = {
            'subtitle': forms.TextInput(attrs={'placeholder': 'Optional subtitle'}),
            'link_url': forms.URLInput(attrs={'placeholder': 'Optional link URL'}),
        }