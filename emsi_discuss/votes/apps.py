"""
Configuration de l'application Votes
"""
from django.apps import AppConfig


class VotesConfig(AppConfig):
    """
    Configuration de l'application Votes
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'votes'
    verbose_name = 'Système de votes'
