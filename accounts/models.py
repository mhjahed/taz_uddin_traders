# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Superadmin'),
        ('owner', 'Owner'),
        ('client', 'Client'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_owner(self):
        return self.role == 'owner'
    
    def is_client(self):
        return self.role == 'client'