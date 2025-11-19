# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from shop.models import Product, Category
from services.models import Request, Service
from .models import Banner
from .forms import BannerForm

def is_owner_or_superadmin(user):
    return user.is_authenticated and (user.is_owner() or user.is_superadmin())

class HomeView(TemplateView):
    template_name = 'public/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(position='home', is_active=True)
        context['featured_categories'] = Category.objects.all()[:6]
        context['featured_products'] = Product.objects.filter(
            is_active=True
        ).order_by('-created_at')[:8]
        return context

class OwnerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'owner/dashboard.html'
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['low_stock_products'] = Product.objects.filter(stock_quantity__lt=10).count()
        context['total_requests'] = Request.objects.count()
        context['pending_requests'] = Request.objects.filter(status='pending').count()
        context['recent_requests'] = Request.objects.order_by('-created_at')[:5]
        context['low_stock_items'] = Product.objects.filter(
            stock_quantity__lt=10
        ).order_by('stock_quantity')[:5]
        return context

class OwnerBannerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Banner
    template_name = 'owner/banner_list.html'
    context_object_name = 'banners'
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class BannerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'owner/banner_form.html'
    success_url = reverse_lazy('core:owner_banner_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class BannerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'owner/banner_form.html'
    success_url = reverse_lazy('core:owner_banner_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class BannerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Banner
    template_name = 'owner/banner_confirm_delete.html'
    success_url = reverse_lazy('core:owner_banner_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Here you would normally send an email
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('core:contact')
    
    return render(request, 'public/contact.html')