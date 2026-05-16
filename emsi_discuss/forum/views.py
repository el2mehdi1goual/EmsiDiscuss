"""
Vues pour l'application Forum
Gestion des sujets du forum : CRUD complet avec filtres
Gestion des réponses et votes
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
from django.db import transaction

from .models import Category, SubCategory, Topic, Tag, Reply
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


def get_subcategories_by_category(request, category_id):
    """
    API endpoint pour récupérer les sous-catégories d'une catégorie
    Retourne JSON avec liste des sous-catégories
    """
    try:
        category = get_object_or_404(Category, id=category_id)
        subcategories = category.subcategories.values('id', 'name').order_by('name')
        return JsonResponse({
            'success': True,
            'subcategories': list(subcategories)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


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
    Recherche : titre, contenu, ou tags (avec ou sans #)
    """
    topics = Topic.objects.select_related('author', 'subcategory__category').prefetch_related('tags')
    
    # Filtres GET
    category_ids = request.GET.getlist('category')
    subcategory_id = request.GET.get('subcategory')
    tag_id = request.GET.get('tag')
    status_filters = request.GET.getlist('status')
    search = request.GET.get('search', '').strip()

    # Appliquer les filtres
    if category_ids:
        topics = topics.filter(subcategory__category_id__in=category_ids)
    
    if subcategory_id:
        topics = topics.filter(subcategory_id=subcategory_id)
    
    if tag_id:
        topics = topics.filter(tags__id=tag_id)
    
    # Filtre statut : résolu, verrouillé, ouvert (multi-sélection)
    if status_filters:
        from django.db.models import Q
        status_query = Q()
        
        if 'solved' in status_filters:
            status_query |= Q(is_solved=True)
        if 'locked' in status_filters:
            status_query |= Q(is_locked=True)
        if 'open' in status_filters:
            status_query |= Q(is_solved=False, is_locked=False)
        
        topics = topics.filter(status_query)
    
    # Recherche texte (titre, contenu, ou tags)
    if search:
        # Nettoyer la recherche (enlever # si présent)
        search_clean = search.lstrip('#').lower()
        
        # Chercher dans titre, contenu, ou tags
        from django.db.models import Q
        topics = topics.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(tags__name__iexact=search_clean)
        ).distinct()
    
    # Récupérer les filtres pour l'affichage
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    tags = Tag.objects.all()
    
    # Compter les totaux pour les statistiques
    total_topics = Topic.objects.count()
    total_replies = Reply.objects.count()
    total_users = __import__('django.contrib.auth.models', fromlist=['User']).User.objects.count()

    context = {
        'page_title': 'Liste des Sujets - Forum',
        'topics': topics,
        'categories': categories,
        'subcategories': subcategories,
        'tags': tags,
        'selected_categories': category_ids,
        'current_subcategory': subcategory_id,
        'current_tag': tag_id,
        'selected_status': status_filters,
        'search_query': search,
        'total_topics': total_topics,
        'total_replies': total_replies,
        'total_users': total_users,
    }
    return render(request, 'forum/topic_list.html', context)


def topic_detail(request, topic_id):
    """
    Vue pour afficher le détail d'un sujet avec ses réponses
    Incrémente le nombre de vues
    Masque les contenus s'ils sont cachés (sauf pour modérateurs/auteur)
    """
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Vérifier si le sujet est masqué (sauf pour modérateurs/auteur)
    is_moderator = request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role in ['moderator', 'admin'])
    if topic.is_hidden and request.user != topic.author and not is_moderator:
        raise Http404("Ce sujet a été masqué.")
    
    replies = topic.replies.select_related('author').prefetch_related('votes', 'quotes')
    
    # Filtrer les réponses masquées (sauf pour modérateurs/auteur)
    if not (request.user == topic.author or is_moderator):
        replies = replies.filter(is_hidden=False)
    
    # Incrémenter les vues (sauf si c'est l'auteur)
    if request.user != topic.author:
        topic.increment_views()
    
    # Calculer les votes pour chaque réponse
    for reply in replies:
        reply.vote_score = sum([v.value for v in reply.votes.all()])
        reply.user_vote = reply.votes.filter(user=request.user).first() if request.user.is_authenticated else None
    
    # Calculer les votes du topic
    topic.vote_score = sum([v.value for v in topic.votes.all()])
    topic.user_vote = topic.votes.filter(user=request.user).first() if request.user.is_authenticated else None
    
    context = {
        'page_title': f'{topic.title} - Forum',
        'topic': topic,
        'replies': replies,
        'category': topic.get_category(),
        'is_moderator': is_moderator,
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
            subcategory = form.cleaned_data.get('subcategory')
            new_subcategory_name = form.cleaned_data.get('new_subcategory_name', '').strip()
            tag_names_str = form.cleaned_data.get('tag_names', '')
            
            # Déterminer la sous-catégorie à utiliser
            if new_subcategory_name:
                # Créer une nouvelle sous-catégorie
                from django.utils.text import slugify
                subcategory, created = SubCategory.objects.get_or_create(
                    category=category,
                    name=new_subcategory_name,
                    defaults={'slug': slugify(new_subcategory_name)}
                )
            elif not subcategory:
                # Pas de sélection, ne devrait pas arriver ici (validé en clean)
                messages.error(request, 'Vous devez sélectionner ou créer une sous-catégorie.')
                return render(request, 'forum/topic_create.html', {
                    'page_title': 'Créer un Sujet',
                    'form': form,
                    'action': 'Créer',
                })
            
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


# ============ RÉPONSES ============

@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def reply_create(request, topic_id):
    """
    Créer une réponse à un sujet
    Supporte les citations
    Vérifie que l'utilisateur n'est pas banni et que le sujet n'est pas verrouillé
    """
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Vérifier que l'utilisateur n'est pas banni
    from django.utils import timezone
    if request.user.profile.is_banned:
        if request.user.profile.banned_until and request.user.profile.banned_until > timezone.now():
            messages.error(request, 'Vous avez été banni de participer au forum.')
            return redirect('forum:topic_detail', topic_id=topic.id)
        else:
            # Débannir si le bannissement a expiré
            request.user.profile.is_banned = False
            request.user.profile.banned_until = None
            request.user.profile.save()
    
    # Vérifier que le sujet n'est pas verrouillé
    if topic.is_locked:
        messages.error(request, 'Ce sujet est verrouillé et ne peut pas recevoir de réponses.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    content = request.POST.get('content', '').strip()
    quoted_reply_id = request.POST.get('quoted_reply_id')
    
    if not content:
        messages.error(request, 'La réponse ne peut pas être vide.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    quoted_reply = None
    if quoted_reply_id:
        quoted_reply = get_object_or_404(Reply, id=quoted_reply_id, topic=topic)
    
    # Créer la réponse
    reply = Reply.objects.create(
        author=request.user,
        topic=topic,
        content=content,
        quoted_reply=quoted_reply
    )
    
    # Créer une notification pour l'auteur du topic
    if request.user != topic.author:
        from notifications.models import Notification
        Notification.objects.create(
            user=topic.author,
            actor=request.user,
            message=f"{request.user.username} a répondu à votre sujet: {topic.title}",
            notification_type='reply',
            topic=topic,
            reply=reply
        )
    
    messages.success(request, 'Votre réponse a été postée avec succès !')
    return redirect('forum:topic_detail', topic_id=topic.id)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def reply_update(request, reply_id):
    """
    Modifier une réponse
    Seul l'auteur peut modifier
    """
    reply = get_object_or_404(Reply, id=reply_id)
    
    # Vérifier les permissions
    if request.user != reply.author and not request.user.is_staff:
        messages.error(request, 'Vous ne pouvez modifier que vos propres réponses.')
        return redirect('forum:topic_detail', topic_id=reply.topic.id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, 'La réponse ne peut pas être vide.')
            return redirect('forum:topic_detail', topic_id=reply.topic.id)
        
        reply.content = content
        reply.save()
        messages.success(request, 'Votre réponse a été modifiée.')
        return redirect('forum:topic_detail', topic_id=reply.topic.id)
    
    context = {
        'page_title': 'Modifier la Réponse',
        'reply': reply,
        'topic': reply.topic,
    }
    return render(request, 'forum/reply_update.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def reply_delete(request, reply_id):
    """
    Supprimer une réponse
    Seul l'auteur ou un admin peut supprimer
    """
    reply = get_object_or_404(Reply, id=reply_id)
    topic = reply.topic
    
    # Vérifier les permissions
    if request.user != reply.author and not request.user.is_staff:
        messages.error(request, 'Vous ne pouvez supprimer que vos propres réponses.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Votre réponse a été supprimée.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    context = {
        'page_title': 'Supprimer la Réponse',
        'reply': reply,
        'topic': topic,
    }
    return render(request, 'forum/reply_delete.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def mark_best_answer(request, reply_id):
    """
    Marquer une réponse comme meilleure réponse
    Seul l'auteur du topic peut faire ça
    """
    reply = get_object_or_404(Reply, id=reply_id)
    topic = reply.topic
    
    # Vérifier que l'utilisateur est l'auteur du topic
    if request.user != topic.author and not request.user.is_staff:
        messages.error(request, 'Seul l\'auteur du sujet peut marquer une meilleure réponse.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    with transaction.atomic():
        # Enlever l'ancien best answer
        old_best = topic.replies.filter(is_best_answer=True).first()
        if old_best:
            old_best.is_best_answer = False
            old_best.save()
            # Retirer les points de réputation
            old_best.author.profile.reputation -= 25
            old_best.author.profile.save()
        
        # Marquer la nouvelle meilleure réponse
        reply.is_best_answer = True
        reply.save()
        
        # Marquer le topic comme résolu
        topic.is_solved = True
        topic.save()
        
        # Ajouter les points de réputation
        reply.author.profile.reputation += 25
        reply.author.profile.save()
        
        # Créer une notification
        from notifications.models import Notification
        Notification.objects.create(
            user=reply.author,
            actor=request.user,
            message=f"Votre réponse à \"{topic.title}\" a été marquée comme meilleure réponse !",
            notification_type='best_answer',
            topic=topic,
            reply=reply
        )
    
    messages.success(request, 'Réponse marquée comme meilleure réponse !')
    return redirect('forum:topic_detail', topic_id=topic.id)

