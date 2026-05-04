"""
Modèles pour l'application Accounts
"""
from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('user', 'Utilisateur'),
    ('moderator', 'Modérateur'),
    ('admin', 'Administrateur'),
]


class Profile(models.Model):
    """
    Profil utilisateur lié en OneToOne avec le modèle User natif de Django
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Avatar de l'utilisateur")
    bio = models.TextField(blank=True, max_length=500, help_text="Biographie courte")
    signature = models.CharField(max_length=255, blank=True, help_text="Signature de l'utilisateur")
    filiere = models.CharField(max_length=100, blank=True, help_text="Filière d'études")
    promotion = models.CharField(max_length=50, blank=True, help_text="Année de promotion")
    reputation = models.IntegerField(default=0, help_text="Points de réputation")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', help_text="Rôle utilisateur")
    is_banned = models.BooleanField(default=False, help_text="Utilisateur banni?")
    banned_until = models.DateTimeField(null=True, blank=True, help_text="Date de fin du bannissement")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return f"Profil de {self.user.username}"

    def get_avatar_url(self):
        """Retourne l'URL de l'avatar ou une image par défaut"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'
