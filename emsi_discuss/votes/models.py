"""
Modèles pour l'application Votes
"""
from django.db import models
from django.contrib.auth.models import User
from forum.models import Reply


class Vote(models.Model):
    """
    Système de votes pour les réponses (utile/pas utile)
    """
    VOTE_CHOICES = [
        (1, 'Utile'),
        (-1, 'Pas utile'),
    ]
    
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ('reply', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Vote de {self.user} sur réponse {self.reply.id}"
