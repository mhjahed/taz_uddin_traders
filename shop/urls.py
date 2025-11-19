# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Public URLs
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Owner URLs
    path('owner/products/', views.OwnerProductListView.as_view(), name='owner_product_list'),
    path('owner/products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('owner/products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('owner/products/<int:pk>/stock/', views.update_stock, name='update_stock'),
]