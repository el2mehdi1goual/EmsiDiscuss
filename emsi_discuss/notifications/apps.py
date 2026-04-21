"""
Configuration de l'application Notifications
"""
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    Configuration de l'application Notifications
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Système de notifications'
