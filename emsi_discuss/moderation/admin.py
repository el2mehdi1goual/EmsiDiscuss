"""
Administration pour l'application Moderation
"""
from django.contrib import admin
from .models import Report, Ban


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Report
    """
    list_display = ('reporter', 'reason', 'is_resolved', 'created_at')
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = ('reporter__username', 'description')
    readonly_fields = ('created_at',)


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Ban
    """
    list_display = ('user', 'is_active', 'banned_by', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
