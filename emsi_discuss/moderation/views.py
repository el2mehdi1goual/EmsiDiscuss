"""
Vues pour l'application Moderation
Gestion des signalements, masquage de contenu, verrouillage de sujets
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Report
from forum.models import Topic, Reply
from .forms import ReportForm, ModerationActionForm


def is_moderator(user):
    """Vérifie si l'utilisateur est modérateur ou admin"""
    return user.is_staff or (hasattr(user, 'profile') and user.profile.role in ['moderator', 'admin'])


@login_required(login_url='accounts:login')
def report_content(request, content_type_name, object_id):
    """
    Vue pour signaler un sujet ou une réponse
    content_type_name: 'topic' ou 'reply'
    """
    # Récupérer le contenu
    if content_type_name == 'topic':
        content_object = get_object_or_404(Topic, id=object_id)
        content_type = ContentType.objects.get(model='topic')
    elif content_type_name == 'reply':
        content_object = get_object_or_404(Reply, id=object_id)
        content_type = ContentType.objects.get(model='reply')
    else:
        raise Http404("Type de contenu invalide")

    # L'utilisateur ne peut pas signaler son propre contenu
    if request.user == content_object.author:
        messages.error(request, 'Vous ne pouvez pas signaler votre propre contenu.')
        if content_type_name == 'topic':
            return redirect('forum:topic_detail', topic_id=object_id)
        else:
            return redirect('forum:topic_detail', topic_id=content_object.topic.id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.content_type = content_type
            report.object_id = object_id
            report.save()
            
            # Créer une notification pour l'auteur du contenu signalé
            from notifications.views import create_report_notification
            create_report_notification(content_object.author, report)
            
            messages.success(request, 'Merci ! Votre signalement a été transmis aux modérateurs.')
            if content_type_name == 'topic':
                return redirect('forum:topic_detail', topic_id=object_id)
            else:
                return redirect('forum:topic_detail', topic_id=content_object.topic.id)
        else:
            messages.error(request, 'Erreur lors du signalement.')
    else:
        form = ReportForm()

    context = {
        'page_title': f'Signaler un {content_type_name}',
        'form': form,
        'content_object': content_object,
        'content_type_name': content_type_name,
    }
    return render(request, 'moderation/report_form.html', context)


@login_required(login_url='accounts:login')
def reports_list(request):
    """
    Liste des signalements - accessible seulement aux modérateurs
    """
    if not is_moderator(request.user):
        messages.error(request, 'Accès réservé aux modérateurs.')
        return redirect('forum:home')

    # Filtrer par statut
    status_filter = request.GET.get('status', 'pending')
    if status_filter in ['pending', 'reviewed', 'resolved', 'rejected']:
        reports = Report.objects.filter(status=status_filter)
    else:
        reports = Report.objects.all()

    # Ordonner par date de création
    reports = reports.order_by('-created_at')

    context = {
        'page_title': 'Signalements - Modération',
        'reports': reports,
        'current_status': status_filter,
    }
    return render(request, 'moderation/reports_list.html', context)


@login_required(login_url='accounts:login')
def report_detail(request, report_id):
    """
    Détail d'un signalement avec actions possibles
    Accessible seulement aux modérateurs
    """
    if not is_moderator(request.user):
        messages.error(request, 'Accès réservé aux modérateurs.')
        return redirect('forum:home')

    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('resolution_notes', '').strip()

        with transaction.atomic():
            if action == 'hide':
                # Masquer le contenu signalé
                content = report.content_object
                if isinstance(content, Topic):
                    content.is_hidden = True
                    content.hidden_reason = f"Signalement: {report.get_reason_display()}"
                    content.save()
                    messages.success(request, 'Le sujet a été masqué.')
                elif isinstance(content, Reply):
                    content.is_hidden = True
                    content.hidden_reason = f"Signalement: {report.get_reason_display()}"
                    content.save()
                    messages.success(request, 'La réponse a été masquée.')
                
                report.mark_as_resolved(request.user, f"Contenu masqué. {notes}")

            elif action == 'ban':
                # Bannir l'auteur temporairement
                author = report.content_object.author
                from datetime import timedelta
                author.profile.is_banned = True
                author.profile.banned_until = timezone.now() + timedelta(days=7)
                author.profile.save()
                
                messages.success(request, f'Utilisateur {author.username} banni pour 7 jours.')
                report.mark_as_resolved(request.user, f"Auteur banni. {notes}")

            elif action == 'approve':
                # Approuver (ne rien faire, juste marquer comme révisé)
                report.mark_as_reviewed(request.user)
                messages.info(request, 'Signalement marqué comme examiné.')

            elif action == 'reject':
                # Rejeter le signalement
                report.status = 'rejected'
                report.reviewed_by = request.user
                report.resolution_notes = notes
                report.reviewed_at = timezone.now()
                report.save()
                messages.info(request, 'Signalement rejeté.')

        return redirect('moderation:reports_list')

    context = {
        'page_title': 'Détail du Signalement',
        'report': report,
        'content_object': report.content_object,
    }
    return render(request, 'moderation/report_detail.html', context)
