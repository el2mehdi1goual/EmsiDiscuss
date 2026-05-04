"""
Vues pour l'application Accounts
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register(request):
    """
    Vue d'inscription
    Affiche le formulaire d'inscription et crée un nouvel utilisateur
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
        else:
            # Afficher les erreurs du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'page_title': 'Inscription',
    }
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    Vue de connexion
    Authentifie l'utilisateur et crée une session
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            # Rediriger vers la page demandée ou vers le profil
            next_page = request.GET.get('next', 'accounts:profile')
            return redirect(next_page)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    context = {
        'page_title': 'Connexion',
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def user_logout(request):
    """
    Vue de déconnexion
    Déconnecte l'utilisateur et redirige vers la page d'accueil
    """
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home')


@login_required(login_url='accounts:login')
def profile(request, username=None):
    """
    Vue de profil utilisateur
    Affiche le profil d'un utilisateur (par défaut l'utilisateur connecté)
    """
    if username:
        # Afficher le profil d'un autre utilisateur
        user = get_object_or_404(User, username=username)
    else:
        # Afficher le profil de l'utilisateur connecté
        user = request.user

    profile = user.profile
    is_own_profile = (user == request.user)

    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'page_title': f'Profil de {user.username}',
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def edit_profile(request):
    """
    Vue pour modifier le profil utilisateur
    Permet de modifier les informations de User et Profile
    """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du profil.')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Modifier mon profil',
    }
    return render(request, 'accounts/edit_profile.html', context)

