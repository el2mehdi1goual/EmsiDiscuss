"""
Administration pour l'application Accounts
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition')
    search_fields = ('name',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'reputation', 'is_banned')
    list_filter = ('role', 'is_banned', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'filiere')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('avatar', 'bio', 'signature', 'filiere', 'promotion', 'reputation', 'role', 'is_banned', 'banned_until', 'badges')}),
    )
