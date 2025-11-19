# services/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Service, Request, RequestReply
from .forms import ServiceForm, RequestForm, RequestReplyForm
from core.models import Banner

def is_owner_or_superadmin(user):
    return user.is_authenticated and (user.is_owner() or user.is_superadmin())

# Public Views
class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(position='services', is_active=True)
        return context

class ClientRequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'services/request_form.html'
    success_url = reverse_lazy('services:request_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.kwargs.get('service_id')
        if service_id:
            context['service'] = Service.objects.get(pk=service_id)
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        service_id = self.kwargs.get('service_id')
        if service_id:
            form.instance.service_id = service_id
        messages.success(self.request, 'Your request has been submitted successfully!')
        return super().form_valid(form)

class ClientRequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'services/client_request_list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        return Request.objects.filter(
            user=self.request.user
        ).select_related('service').prefetch_related('replies')

@login_required
def client_request_detail(request, pk):
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)
    
    context = {
        'request': request_obj,
        'replies': request_obj.replies.all()
    }
    return render(request, 'services/client_request_detail.html', context)

# Owner Views
class OwnerServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = 'owner/service_list.html'
    context_object_name = 'services'
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'owner/service_form.html'
    success_url = reverse_lazy('services:owner_service_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'owner/service_form.html'
    success_url = reverse_lazy('services:owner_service_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)

class OwnerRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Request
    template_name = 'owner/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        service_type = self.request.GET.get('service_type')
        
        if status:
            queryset = queryset.filter(status=status)
        if service_type:
            queryset = queryset.filter(service__service_type=service_type)
            
        return queryset.select_related('user', 'service').prefetch_related('replies')

@login_required
@user_passes_test(is_owner_or_superadmin)
def owner_request_detail(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        form = RequestReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.request = request_obj
            reply.user = request.user
            reply.save()
            
            # Update request status
            new_status = request.POST.get('status')
            if new_status:
                request_obj.status = new_status
                request_obj.save()
            
            messages.success(request, 'Reply sent successfully!')
            return redirect('services:owner_request_detail', pk=pk)
    else:
        form = RequestReplyForm()
    
    context = {
        'request': request_obj,
        'form': form,
        'replies': request_obj.replies.all()
    }
    return render(request, 'owner/request_detail.html', context)