# services/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    SERVICE_TYPES = (
        ('membership', 'Membership'),
        ('appointment', 'Appointment (In-person)'),
        ('online_appointment', 'Online Appointment'),
        ('order', 'Order Placement'),
        ('complaint', 'Complaint Submission'),
        ('fast_track', 'Fast Track Help'),
        ('general', 'General Request'),
    )
    
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"

class RequestReply(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']