"""
Administration pour l'application Votes
"""
from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Vote
    """
    list_display = ('user', 'reply', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'reply__id')
    readonly_fields = ('created_at',)
