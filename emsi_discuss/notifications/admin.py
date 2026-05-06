"""
Administration pour l'application Notifications
"""
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'actor', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'actor__username', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Notification', {
            'fields': ('user', 'actor', 'message', 'notification_type')
        }),
        ('Références', {
            'fields': ('topic', 'reply', 'report'),
            'classes': ('collapse',)
        }),
        ('État', {
            'fields': ('is_read', 'created_at'),
        }),
    )
    raw_id_fields = ('topic', 'reply', 'report', 'actor')
