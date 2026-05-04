"""
Signaux pour l'application Accounts
Crée automatiquement un profil quand un utilisateur est créé ou mis à jour
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal pour créer automatiquement un Profile quand un User est créé
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal pour sauvegarder automatiquement le Profile quand l'User est sauvegardé
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
