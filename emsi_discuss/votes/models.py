"""
Modèles pour l'application Votes
"""
from django.db import models
from django.conf import settings
from forum.models import Topic, Reply


class TopicVote(models.Model):
    """
    Système de votes pour les sujets
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_votes')
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote sur Sujet'
        verbose_name_plural = 'Votes sur Sujets'
        unique_together = ('topic', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Vote de {self.user} sur sujet {self.topic.id}"


class ReplyVote(models.Model):
    """
    Système de votes pour les réponses
    """
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reply_votes')
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote sur Réponse'
        verbose_name_plural = 'Votes sur Réponses'
        unique_together = ('reply', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Vote de {self.user} sur réponse {self.reply.id}"
