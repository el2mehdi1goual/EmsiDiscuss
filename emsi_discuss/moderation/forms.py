"""
Formulaires pour l'application Moderation
"""
from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    """
    Formulaire pour signaler un contenu
    """
    class Meta:
        model = Report
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-control',
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez pourquoi vous signalez ce contenu...',
            }),
        }
        labels = {
            'reason': 'Raison du signalement',
            'details': 'Détails supplémentaires',
        }


class ModerationActionForm(forms.Form):
    """
    Formulaire pour les actions de modération
    """
    ACTION_CHOICES = [
        ('hide', 'Masquer le contenu'),
        ('ban', 'Bannir l\'auteur'),
        ('approve', 'Approuver'),
        ('reject', 'Rejeter'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect,
        label='Action'
    )
    resolution_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notes de résolution (optionnel)...',
        }),
        label='Notes de résolution'
    )
