"""
Modèles pour l'application Accounts
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class Badge(models.Model):
    """
    Badge utilisateur
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé correspondant au diagramme UML
    """
    avatar = models.URLField(blank=True, help_text="URL de l'image d'avatar")
    bio = models.TextField(blank=True)
    signature = models.TextField(blank=True)
    filiere = models.CharField(max_length=100, blank=True)
    promotion = models.CharField(max_length=50, blank=True)
    reputation = models.IntegerField(default=0)
    role = models.CharField(max_length=50, default='student')
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True, blank=True)
    badges = models.ManyToManyField(Badge, blank=True, related_name='users')

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username
