"""
Vues pour l'application Forum
"""
from django.shortcuts import render
from .models import Category, Topic


def forum_home(request):
    """
    Vue d'accueil du forum - affiche les catégories
    """
    categories = Category.objects.all()
    context = {
        'app_name': 'Forum',
        'categories': categories,
    }
    return render(request, 'forum/home.html', context)
