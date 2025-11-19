# services/forms.py
from django import forms
from .models import Service, Request, RequestReply

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'service_type', 'description', 'icon', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'icon': forms.TextInput(attrs={'placeholder': 'e.g., fas fa-users'})
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5})
        }

class RequestReplyForm(forms.ModelForm):
    class Meta:
        model = RequestReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your reply here...'})
        }