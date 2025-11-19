# services/admin.py
from django.contrib import admin
from .models import Service, Request, RequestReply

class RequestReplyInline(admin.TabularInline):
    model = RequestReply
    extra = 0
    readonly_fields = ('user', 'created_at')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'service', 'status', 'created_at')
    list_filter = ('status', 'service__service_type', 'created_at')
    search_fields = ('subject', 'message', 'user__username')
    inlines = [RequestReplyInline]