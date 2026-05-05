"""
Vues pour l'application Forum
Gestion des sujets du forum : CRUD complet avec filtres
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify

from .models import Category, SubCategory, Topic, Tag
from .forms import TopicCreateForm, TopicUpdateForm


def parse_tag_names(tag_names_str):
    """
    Parse une chaîne de tags et retourne une liste de noms de tags nettoyés
    Accepte des tags séparés par des espaces, avec ou sans #
    Exemple: "#python #django #bug" ou "python django bug"
    """
    if not tag_names_str:
        return []
    
    # Diviser par espaces
    tags = tag_names_str.split()
    
    # Nettoyer chaque tag (enlever # et espaces)
    cleaned_tags = []
    for tag in tags:
        tag = tag.strip().lstrip('#').strip()
        if tag:  # Si après nettoyage il reste quelque chose
            cleaned_tags.append(tag)
    
    return cleaned_tags


def get_or_create_tags(tag_names_list):
    """
    Récupère ou crée les tags à partir d'une liste de noms
    Retourne une liste d'objets Tag
    """
    tags = []
    for tag_name in tag_names_list:
        tag_name = tag_name.strip()
        if tag_name:
            # Créer ou récupérer le tag
            tag, created = Tag.objects.get_or_create(
                name__iexact=tag_name,  # Case-insensitive
                defaults={'name': tag_name, 'slug': slugify(tag_name)}
            )
            tags.append(tag)
    
    return tags


def forum_home(request):
    """
    Vue d'accueil du forum - affiche les catégories et résumé
    """
    categories = Category.objects.all().prefetch_related('subcategories')
    topics_count = Topic.objects.count()
    
    context = {
        'page_title': 'Forum - EMSI_Discuss',
        'categories': categories,
        'topics_count': topics_count,
    }
    return render(request, 'forum/home.html', context)


def topic_list(request):
    """
    Vue pour lister tous les sujets avec filtres
    Filtres disponibles : catégorie, sous-catégorie, tag, statut
    """
    topics = Topic.objects.select_related('author', 'subcategory__category').prefetch_related('tags')
    
    # Filtres GET
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    tag_id = request.GET.get('tag')
    status_filter = request.GET.get('status')
    search = request.GET.get('search')

    # Appliquer les filtres
    if category_id:
        topics = topics.filter(subcategory__category_id=category_id)
    
    if subcategory_id:
        topics = topics.filter(subcategory_id=subcategory_id)
    
    if tag_id:
        topics = topics.filter(tags__id=tag_id)
    
    # Filtre statut : résolu, verrouillé, ouvert
    if status_filter == 'solved':
        topics = topics.filter(is_solved=True)
    elif status_filter == 'locked':
        topics = topics.filter(is_locked=True)
    elif status_filter == 'open':
        topics = topics.filter(is_solved=False, is_locked=False)
    
    # Recherche texte
    if search:
        topics = topics.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search)
        )
    
    # Récupérer les filtres pour l'affichage
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    tags = Tag.objects.all()

    context = {
        'page_title': 'Liste des Sujets - Forum',
        'topics': topics,
        'categories': categories,
        'subcategories': subcategories,
        'tags': tags,
        'current_category': category_id,
        'current_subcategory': subcategory_id,
        'current_tag': tag_id,
        'current_status': status_filter,
        'search_query': search,
    }
    return render(request, 'forum/topic_list.html', context)


def topic_detail(request, topic_id):
    """
    Vue pour afficher le détail d'un sujet
    Incrémente le nombre de vues
    """
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Incrémenter les vues (sauf si c'est l'auteur)
    if request.user != topic.author:
        topic.increment_views()
    
    context = {
        'page_title': f'{topic.title} - Forum',
        'topic': topic,
        'category': topic.get_category(),
    }
    return render(request, 'forum/topic_detail.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def topic_create(request):
    """
    Vue pour créer un nouveau sujet
    Gère la création dynamique de la sous-catégorie et des tags
    Nécessite d'être connecté
    """
    if request.method == 'POST':
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            # Récupérer la catégorie sélectionnée
            category = form.cleaned_data.get('category')
            subcategory_name = form.cleaned_data.get('subcategory_name')
            tag_names_str = form.cleaned_data.get('tag_names', '')
            
            # Créer ou récupérer la sous-catégorie
            subcategory, created = SubCategory.objects.get_or_create(
                category=category,
                name=subcategory_name,
                defaults={'slug': slugify(subcategory_name)}
            )
            
            # Créer le topic sans le sauvegarder tout de suite
            topic = form.save(commit=False)
            topic.author = request.user  # Assigner l'auteur
            topic.subcategory = subcategory  # Assigner la sous-catégorie
            topic.save()  # Sauvegarder le topic
            
            # Parser et créer les tags
            tag_names_list = parse_tag_names(tag_names_str)
            tags = get_or_create_tags(tag_names_list)
            
            # Associer les tags au topic
            topic.tags.set(tags)
            
            messages.success(request, 'Votre sujet a été créé avec succès !')
            return redirect('forum:topic_detail', topic_id=topic.id)
        else:
            messages.error(request, 'Erreur lors de la création du sujet.')
    else:
        form = TopicCreateForm()

    context = {
        'page_title': 'Créer un Sujet',
        'form': form,
        'action': 'Créer',
    }
    return render(request, 'forum/topic_create.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def topic_update(request, topic_id):
    """
    Vue pour modifier un sujet
    Permet de modifier le titre, contenu et tags
    Catégorie et sous-catégorie ne peuvent pas être modifiées
    Seul l'auteur peut modifier son sujet
    """
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Vérifier que l'utilisateur est l'auteur
    if request.user != topic.author and not request.user.is_staff:
        messages.error(request, 'Vous ne pouvez modifier que vos propres sujets.')
        return redirect('forum:topic_detail', topic_id=topic.id)

    if request.method == 'POST':
        form = TopicUpdateForm(request.POST, instance=topic)
        if form.is_valid():
            # Récupérer les tags saisis
            tag_names_str = form.cleaned_data.get('tag_names', '')
            
            # Sauvegarder le topic
            form.save()
            
            # Parser et créer les tags
            tag_names_list = parse_tag_names(tag_names_str)
            tags = get_or_create_tags(tag_names_list)
            
            # Mettre à jour les tags du topic
            topic.tags.set(tags)
            
            messages.success(request, 'Votre sujet a été modifié avec succès !')
            return redirect('forum:topic_detail', topic_id=topic.id)
        else:
            messages.error(request, 'Erreur lors de la modification du sujet.')
    else:
        form = TopicUpdateForm(instance=topic)
        # Pré-remplir le champ tag_names avec les tags actuels
        current_tags = ' '.join([f'#{tag.name}' for tag in topic.tags.all()])
        form.fields['tag_names'].initial = current_tags

    context = {
        'page_title': 'Modifier le Sujet',
        'form': form,
        'topic': topic,
        'action': 'Modifier',
    }
    return render(request, 'forum/topic_update.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def topic_delete(request, topic_id):
    """
    Vue pour supprimer un sujet
    Seul l'auteur ou un admin peut supprimer
    """
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Vérifier que l'utilisateur est l'auteur ou un admin
    if request.user != topic.author and not request.user.is_staff:
        messages.error(request, 'Vous ne pouvez supprimer que vos propres sujets.')
        return redirect('forum:topic_detail', topic_id=topic.id)

    if request.method == 'POST':
        # Confirmer la suppression
        subcategory_id = topic.subcategory.id
        topic.delete()
        messages.success(request, 'Votre sujet a été supprimé.')
        return redirect('forum:topic_list')
    
    # Afficher la page de confirmation
    context = {
        'page_title': 'Supprimer le Sujet',
        'topic': topic,
    }
    return render(request, 'forum/topic_delete.html', context)

