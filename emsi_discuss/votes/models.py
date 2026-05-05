"""
Modèles pour l'application Votes
Système de votes pour les sujets et les réponses
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from forum.models import Topic


class TopicVote(models.Model):
    """
    Système de votes pour les sujets
    utile = 1, pas utile = -1
    """
    VOTE_CHOICES = (
        (1, 'Utile'),
        (-1, 'Pas utile'),
    )
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_votes')
    value = models.IntegerField(choices=VOTE_CHOICES, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    utile = 1, pas utile = -1
    """
    VOTE_CHOICES = (
        (1, 'Utile'),
        (-1, 'Pas utile'),
    )
    
    reply = models.ForeignKey('forum.Reply', on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reply_votes')
    value = models.IntegerField(choices=VOTE_CHOICES, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vote sur Réponse'
        verbose_name_plural = 'Votes sur Réponses'
        unique_together = ('reply', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Vote de {self.user} sur réponse {self.reply.id}"
