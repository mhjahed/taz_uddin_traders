# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import ClientRegistrationForm

class ClientRegistrationView(CreateView):
    form_class = ClientRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful! Welcome to TAZ UDDIN TRADERS.')
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superadmin() or user.is_owner():
            return reverse_lazy('core:owner_dashboard')
        return reverse_lazy('core:home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')