# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.role = 'client'
        if commit:
            user.save()
        return user