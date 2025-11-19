# Create a file: create_sample_data.py in project root

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from shop.models import Category, Product
from services.models import Service
from core.models import Banner

# Create owner user
owner = User.objects.create_user(
    username='owner',
    password='owner123',
    email='owner@tazuddintraders.com',
    role='owner',
    first_name='Shop',
    last_name='Owner'
)

# Create sample categories
categories = [
    {'name': 'Cement', 'icon': 'fas fa-cube'},
    {'name': 'Steel Rods', 'icon': 'fas fa-bars'},
    {'name': 'Ceramics', 'icon': 'fas fa-th'},
    {'name': 'Paints', 'icon': 'fas fa-paint-brush'},
    {'name': 'Electrical', 'icon': 'fas fa-bolt'},
    {'name': 'Plumbing', 'icon': 'fas fa-wrench'},
]

for cat_data in categories:
    Category.objects.create(**cat_data)

# Create sample products
cement_cat = Category.objects.get(name='Cement')
for i in range(1, 6):
    Product.objects.create(
        name=f'Premium Cement Brand {i}',
        category=cement_cat,
        description=f'High quality cement suitable for all construction needs. Brand {i}',
        price=450.00,
        stock_quantity=100 if i % 2 else 5,
        minimum_order=50,
        created_by=owner
    )

# Create services
services_data = [
    {
        'title': 'Bulk Order Membership',
        'service_type': 'membership',
        'description': 'Get exclusive benefits and discounts on bulk orders',
        'icon': 'fas fa-users'
    },
    {
        'title': 'Schedule In-Person Meeting',
        'service_type': 'appointment',
        'description': 'Book an appointment to visit our warehouse',
        'icon': 'fas fa-calendar-alt'
    },
    {
        'title': 'Online Consultation',
        'service_type': 'online_appointment',
        'description': 'Schedule a video call with our experts',
        'icon': 'fas fa-video'
    },
    {
        'title': 'Place Bulk Order',
        'service_type': 'order',
        'description': 'Submit your bulk order requirements',
        'icon': 'fas fa-shopping-cart'
    },
]

for service_data in services_data:
    Service.objects.create(**service_data)

print("Sample data created successfully!")
print("Owner login: username='owner', password='owner123'")