"""
Configuration de l'application Forum
"""
from django.apps import AppConfig


class ForumConfig(AppConfig):
    """
    Configuration de l'application Forum
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'
    verbose_name = 'Forum de discussion'
