# core/models.py
from django.db import models

class Banner(models.Model):
    POSITION_CHOICES = (
        ('home', 'Home Page'),
        ('shop', 'Shop Page'),
        ('services', 'Services Page'),
    )
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    link_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.position}"