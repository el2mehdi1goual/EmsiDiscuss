"""
Modèles pour l'application Moderation
Étape 6 du projet - À développer dans la prochaine phase
"""
from django.db import models
from django.conf import settings
from forum.models import Topic


class Report(models.Model):
    """
    Signalements de contenu inapproprié
    """
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewed', 'Examiné'),
        ('resolved', 'Résolu'),
        ('rejected', 'Rejeté'),
    ]
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_submitted')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']

    def __str__(self):
        return f"Signalement de {self.reporter} - {self.status}"
