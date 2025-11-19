# shop/management/commands/create_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category
from services.models import Service

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates initial categories and services'

    def handle(self, *args, **kwargs):
        # Create default categories
        categories = [
            {'name': 'Cement', 'icon': 'fas fa-cube'},
            {'name': 'Steel Rods', 'icon': 'fas fa-bars'},
            {'name': 'Ceramics', 'icon': 'fas fa-th'},
            {'name': 'Paints', 'icon': 'fas fa-paint-brush'},
            {'name': 'Electrical', 'icon': 'fas fa-bolt'},
            {'name': 'Plumbing', 'icon': 'fas fa-wrench'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(**cat_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))