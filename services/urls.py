# services/urls.py
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Public URLs
    path('', views.ServiceListView.as_view(), name='service_list'),
    path('request/<int:service_id>/', views.ClientRequestCreateView.as_view(), name='create_request'),
    path('my-requests/', views.ClientRequestListView.as_view(), name='request_list'),
    path('my-requests/<int:pk>/', views.client_request_detail, name='client_request_detail'),
    
    # Owner URLs
    path('owner/services/', views.OwnerServiceListView.as_view(), name='owner_service_list'),
    path('owner/services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('owner/services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('owner/requests/', views.OwnerRequestListView.as_view(), name='owner_request_list'),
    path('owner/requests/<int:pk>/', views.owner_request_detail, name='owner_request_detail'),
]