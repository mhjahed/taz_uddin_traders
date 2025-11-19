# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, ProductImageFormSet
from core.models import Banner

def is_owner_or_superadmin(user):
    return user.is_authenticated and (user.is_owner() or user.is_superadmin())

# Public Views
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.select_related('category').prefetch_related('images')
        return Product.objects.filter(is_active=True)\
              .select_related('category', 'created_by')\
              .prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['banners'] = Banner.objects.filter(position='shop', is_active=True)
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = Category.objects.get(slug=category_slug)
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return context

# Owner Views
class OwnerProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'owner/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__id=category)
            
        return queryset.select_related('category')

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'owner/product_form.html'
    success_url = reverse_lazy('shop:owner_product_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ProductImageFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            form.instance.created_by = self.request.user
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'Product created successfully!')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'owner/product_form.html'
    success_url = reverse_lazy('shop:owner_product_list')
    
    def test_func(self):
        return is_owner_or_superadmin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context['image_formset'] = ProductImageFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.save()
            messages.success(self.request, 'Product updated successfully!')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

@login_required
@user_passes_test(is_owner_or_superadmin)
def update_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        stock_quantity = request.POST.get('stock_quantity')
        if stock_quantity:
            product.stock_quantity = int(stock_quantity)
            product.save()
            messages.success(request, f'Stock updated for {product.name}')
    
    return redirect('shop:owner_product_list')