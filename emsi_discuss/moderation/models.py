"""
Modèles pour l'application Moderation
Gestion des signalements et contenus inappropriés
"""
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Report(models.Model):
    """
    Signalements de contenu inapproprié (Topic ou Reply)
    Utilise GenericForeignKey pour supporter multiple modèles
    """
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Contenu inapproprié'),
        ('harassment', 'Harcèlement'),
        ('misinformation', 'Désinformation'),
        ('copyright', 'Violation de droits'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewed', 'Examiné'),
        ('resolved', 'Résolu'),
        ('rejected', 'Rejeté'),
    ]
    
    # Reporter
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reports_submitted'
    )
    
    # Contenu signalé (GenericForeignKey pour Topic ou Reply)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Raison et détails
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default='other')
    details = models.TextField(blank=True, help_text="Détails supplémentaires du signalement")
    
    # Statut et gestion
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    resolution_notes = models.TextField(blank=True, help_text="Notes de résolution")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"Signalement de {self.reporter} - {self.get_reason_display()} - {self.status}"
    
    def get_content_type_name(self):
        """Retourne le type de contenu (Topic ou Reply)"""
        return self.content_type.model.capitalize()
    
    def mark_as_resolved(self, moderator, notes=''):
        """Marque le rapport comme résolu"""
        from django.utils import timezone
        self.status = 'resolved'
        self.reviewed_by = moderator
        self.resolution_notes = notes
        self.reviewed_at = timezone.now()
        self.save()
    
    def mark_as_reviewed(self, moderator):
        """Marque le rapport comme examiné"""
        from django.utils import timezone
        self.status = 'reviewed'
        self.reviewed_by = moderator
        self.reviewed_at = timezone.now()
        self.save()
