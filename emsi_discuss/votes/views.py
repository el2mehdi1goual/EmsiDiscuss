"""
Vues pour l'application Votes
Gestion des votes sur les topics et réponses
"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction

from forum.models import Topic, Reply
from .models import TopicVote, ReplyVote


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def vote_topic(request, topic_id):
    """
    Voter sur un sujet
    value: 1 (utile) ou -1 (pas utile)
    """
    topic = get_object_or_404(Topic, id=topic_id)
    value = int(request.POST.get('value', 0))
    
    if value not in [1, -1]:
        messages.error(request, 'Vote invalide.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    with transaction.atomic():
        # Chercher un vote existant
        existing_vote = TopicVote.objects.filter(topic=topic, user=request.user).first()
        
        if existing_vote:
            # Si c'est le même vote, l'annuler
            if existing_vote.value == value:
                old_value = existing_vote.value
                existing_vote.delete()
                # Retirer les points
                topic.author.profile.reputation -= (5 if old_value == 1 else 2)
            else:
                # Mettre à jour le vote
                old_value = existing_vote.value
                existing_vote.value = value
                existing_vote.save()
                # Ajuster les points
                diff = 0
                if old_value == 1 and value == -1:
                    diff = -7  # -5 +(-2)
                elif old_value == -1 and value == 1:
                    diff = 7  # -(-2) + 5
                topic.author.profile.reputation += diff
        else:
            # Créer un nouveau vote
            TopicVote.objects.create(topic=topic, user=request.user, value=value)
            # Ajouter les points
            topic.author.profile.reputation += (5 if value == 1 else -2)
        
        # Sauvegarder la réputation
        topic.author.profile.save()
    
    # Calculer le score
    vote_score = sum([v.value for v in topic.votes.all()])
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'vote_score': vote_score,
            'user_vote': request.POST.get('value'),
        })
    
    return redirect('forum:topic_detail', topic_id=topic.id)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def vote_reply(request, reply_id):
    """
    Voter sur une réponse
    value: 1 (utile) ou -1 (pas utile)
    """
    reply = get_object_or_404(Reply, id=reply_id)
    topic = reply.topic
    value = int(request.POST.get('value', 0))
    
    if value not in [1, -1]:
        messages.error(request, 'Vote invalide.')
        return redirect('forum:topic_detail', topic_id=topic.id)
    
    with transaction.atomic():
        # Chercher un vote existant
        existing_vote = ReplyVote.objects.filter(reply=reply, user=request.user).first()
        
        if existing_vote:
            # Si c'est le même vote, l'annuler
            if existing_vote.value == value:
                old_value = existing_vote.value
                existing_vote.delete()
                # Retirer les points
                reply.author.profile.reputation -= (10 if old_value == 1 else 2)
            else:
                # Mettre à jour le vote
                old_value = existing_vote.value
                existing_vote.value = value
                existing_vote.save()
                # Ajuster les points
                diff = 0
                if old_value == 1 and value == -1:
                    diff = -12  # -10 +(-2)
                elif old_value == -1 and value == 1:
                    diff = 12  # -(-2) + 10
                reply.author.profile.reputation += diff
        else:
            # Créer un nouveau vote
            ReplyVote.objects.create(reply=reply, user=request.user, value=value)
            # Ajouter les points
            reply.author.profile.reputation += (10 if value == 1 else -2)
        
        # Sauvegarder la réputation
        reply.author.profile.save()
    
    # Calculer le score
    vote_score = sum([v.value for v in reply.votes.all()])
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'vote_score': vote_score,
            'user_vote': request.POST.get('value'),
        })
    
    return redirect('forum:topic_detail', topic_id=topic.id)
