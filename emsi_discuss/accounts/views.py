"""
Vues pour l'application Accounts
"""
from django.shortcuts import render


def accounts_home(request):
    """
    Vue d'accueil de l'application Accounts
    """
    context = {
        'app_name': 'Accounts',
    }
    return render(request, 'accounts/home.html', context)
