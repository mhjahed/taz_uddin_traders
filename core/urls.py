# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('dashboard/', views.OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('banners/', views.OwnerBannerListView.as_view(), name='owner_banner_list'),
    path('banners/create/', views.BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/update/', views.BannerUpdateView.as_view(), name='banner_update'),
    path('banners/<int:pk>/delete/', views.BannerDeleteView.as_view(), name='banner_delete'),
]