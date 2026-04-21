"""
Administration pour l'application Accounts
"""
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle UserProfile
    """
    list_display = ('user', 'is_banned', 'created_at')
    list_filter = ('is_banned', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
