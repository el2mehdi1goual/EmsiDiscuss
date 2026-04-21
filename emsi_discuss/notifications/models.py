"""
Modèles pour l'application Notifications
"""
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    Système de notifications simples
    """
    NOTIFICATION_CHOICES = [
        ('reply', 'Nouvelle réponse'),
        ('topic', 'Nouveau sujet'),
        ('mention', 'Mention'),
        ('message', 'Message'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification pour {self.user} - {self.type}"
