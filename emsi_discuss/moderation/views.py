"""
Vues pour l'application Moderation
"""
from django.shortcuts import render


def moderation_home(request):
    """
    Vue d'accueil de l'application Moderation
    """
    context = {
        'app_name': 'Moderation',
    }
    return render(request, 'moderation/home.html', context)
