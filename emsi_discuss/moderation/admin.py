"""
Administration pour l'application Moderation
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'content_type', 'get_content_summary', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at', 'content_type')
    search_fields = ('reporter__username', 'reason', 'details')
    readonly_fields = ('created_at', 'reviewed_at', 'content_object')
    
    fieldsets = (
        ('Informations du signalement', {
            'fields': ('reporter', 'content_type', 'object_id', 'content_object'),
        }),
        ('Détails', {
            'fields': ('reason', 'details'),
        }),
        ('Gestion du rapport', {
            'fields': ('status', 'reviewed_by', 'resolution_notes', 'created_at', 'reviewed_at'),
        }),
    )
    
    def get_content_summary(self, obj):
        """Affiche un résumé du contenu signalé"""
        content = obj.content_object
        if content:
            if obj.content_type.model == 'topic':
                return content.title[:50]
            elif obj.content_type.model == 'reply':
                return content.content[:50]
        return 'N/A'
    
    get_content_summary.short_description = 'Contenu'
    
    def save_model(self, request, obj, form, change):
        """Sauvegarde le rapport et met à jour reviewed_by si nécessaire"""
        if obj.status != 'pending' and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)
