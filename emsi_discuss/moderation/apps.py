"""
Configuration de l'application Moderation
"""
from django.apps import AppConfig


class ModerationConfig(AppConfig):
    """
    Configuration de l'application Moderation
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moderation'
    verbose_name = 'Modération du forum'
