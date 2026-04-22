"""
Modèles pour l'application Accounts
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Profil utilisateur étendu
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True, help_text='URL de l\'image d\'avatar')
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateur'

    def __str__(self):
        return f"Profil de {self.user.username}"
