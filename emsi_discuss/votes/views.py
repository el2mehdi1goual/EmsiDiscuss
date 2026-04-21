"""
Vues pour l'application Votes
"""
from django.shortcuts import render


def votes_home(request):
    """
    Vue d'accueil de l'application Votes
    """
    context = {
        'app_name': 'Votes',
    }
    return render(request, 'votes/home.html', context)
