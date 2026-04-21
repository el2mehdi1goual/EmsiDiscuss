"""
Views générales pour le projet emsi_discuss
"""
from django.shortcuts import render


def home(request):
    """
    Vue de la page d'accueil du projet EMSI_Discuss
    
    Contexte:
        - project_name: Nom du projet
        - description: Description courte du projet
        - modules: Liste des applications/modules du projet
    """
    context = {
        'project_name': 'EMSI_Discuss',
        'description': 'Forum de discussion académique pour les étudiants EMSI',
        'modules': [
            {
                'name': 'Accounts',
                'description': 'Gestion des utilisateurs et profils',
                'url': '#'
            },
            {
                'name': 'Forum',
                'description': 'Catégories, sous-catégories, sujets et réponses',
                'url': '#'
            },
            {
                'name': 'Votes',
                'description': 'Système de votes utile / pas utile',
                'url': '#'
            },
            {
                'name': 'Modération',
                'description': 'Signalements, masquage, verrouillage et bannissement',
                'url': '#'
            },
            {
                'name': 'Notifications',
                'description': 'Système de notifications',
                'url': '#'
            },
        ],
        'status': '✓ Base du projet initialisée avec succès',
    }
    return render(request, 'home.html', context)
