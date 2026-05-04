"""
Administration pour l'application Accounts
"""
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Administration du modèle Profile
    """
    list_display = ('get_username', 'role', 'reputation', 'is_banned', 'filiere', 'created_at')
    list_filter = ('role', 'is_banned', 'created_at')
    search_fields = ('user__username', 'user__email', 'filiere', 'promotion')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations Personnelles', {
            'fields': ('avatar', 'bio', 'signature')
        }),
        ('Étudiant', {
            'fields': ('filiere', 'promotion')
        }),
        ('Rôle et Permissions', {
            'fields': ('role', 'reputation')
        }),
        ('Modération', {
            'fields': ('is_banned', 'banned_until')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_username(self, obj):
        """Affiche le nom d'utilisateur en lien vers le profil"""
        return obj.user.username
    get_username.short_description = 'Utilisateur'
