"""
Modèles pour l'application Notifications
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Système de notifications
    """
    NOTIFICATION_TYPES = (
        ('reply', 'Nouvelle réponse'),
        ('vote', 'Vote reçu'),
        ('best_answer', 'Meilleure réponse'),
        ('mention', 'Mention'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='reply')
    
    # Références optionnelles
    topic = models.ForeignKey('forum.Topic', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    reply = models.ForeignKey('forum.Reply', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications_sent')
    
    # État
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification pour {self.user}: {self.message}"
    
    def mark_as_read(self):
        """Marquer comme lue"""
        self.is_read = True
        self.save(update_fields=['is_read'])
