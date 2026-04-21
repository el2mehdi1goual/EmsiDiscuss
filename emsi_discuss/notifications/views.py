"""
Vues pour l'application Notifications
"""
from django.shortcuts import render


def notifications_home(request):
    """
    Vue d'accueil de l'application Notifications
    """
    context = {
        'app_name': 'Notifications',
    }
    return render(request, 'notifications/home.html', context)
