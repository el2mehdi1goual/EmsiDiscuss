"""
Modèles pour l'application Moderation
"""
from django.db import models
from django.contrib.auth.models import User
from forum.models import Topic, Reply


class Report(models.Model):
    """
    Signalements de contenu inapproprié
    """
    REPORT_CHOICES = [
        ('spam', 'Spam'),
        ('offensive', 'Contenu offensant'),
        ('inappropriate', 'Contenu inapproprié'),
        ('other', 'Autre'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=20, choices=REPORT_CHOICES)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']

    def __str__(self):
        return f"Signalement de {self.reporter} - {self.reason}"


class Ban(models.Model):
    """
    Bannissement d'utilisateurs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    banned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bans_issued')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Bannissement'
        verbose_name_plural = 'Bannissements'
        ordering = ['-created_at']

    def __str__(self):
        return f"Ban de {self.user.username}"
