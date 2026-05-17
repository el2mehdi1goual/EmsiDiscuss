"""
Vues pour l'application Notifications
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


@login_required(login_url='accounts:login')
def notification_list(request):
    """
    Liste les notifications de l'utilisateur connecté
    Affiche d'abord les non-lues, puis les lues
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    total_count = notifications.count()
    unread_count = notifications.filter(is_read=False).count()
    read_count = total_count - unread_count

    context = {
        'notifications': notifications,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required(login_url='accounts:login')
def mark_notification_read(request, notification_id):
    """
    Marque une notification comme lue
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    messages.success(request, 'Notification marquée comme lue')
    
    # Retourner vers la page d'où on vient, ou les notifications
    next_url = request.GET.get('next', 'notifications:list')
    return redirect(next_url)


@login_required(login_url='accounts:login')
def mark_all_notifications_read(request):
    """
    Marque toutes les notifications comme lues
    """
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'Toutes les notifications sont marquées comme lues')
    return redirect('notifications:list')


def create_reply_notification(topic_author, reply_author, reply, topic):
    """
    Crée une notification quand quelqu'un répond à un topic
    """
    if topic_author == reply_author:
        # Ne pas créer de notification si c'est l'auteur qui répond
        return
    
    Notification.objects.create(
        user=topic_author,
        actor=reply_author,
        topic=topic,
        reply=reply,
        notification_type='reply',
        message=f"{reply_author.get_full_name() or reply_author.username} a répondu à votre sujet \"{topic.title}\""
    )


def create_report_notification(content_author, report):
    """
    Crée une notification quand un contenu est signalé
    """
    Notification.objects.create(
        user=content_author,
        report=report,
        notification_type='report',
        message=f"Un de vos contenus a été signalé comme {report.get_reason_display()}"
    )


def create_best_answer_notification(reply_author, reply, topic):
    """
    Crée une notification quand une réponse est marquée comme meilleure
    """
    Notification.objects.create(
        user=reply_author,
        topic=topic,
        reply=reply,
        notification_type='best_answer',
        message=f"Votre réponse au sujet \"{topic.title}\" a été marquée comme meilleure réponse"
    )


def create_admin_report_notification(report):
    """
    Crée une notification pour TOUS les admins/modérateurs
    quand un nouveau signalement est créé
    """
    from django.contrib.auth.models import User
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Récupérer tous les admins et modérateurs
        admins_moderators = User.objects.filter(is_staff=True)
        
        logger.info(f"Admins trouvés: {admins_moderators.count()}")
        
        # Créer une notification pour chaque admin/modérateur
        for admin in admins_moderators:
            reporter_name = report.reporter.get_full_name() or report.reporter.username
            
            notif = Notification.objects.create(
                user=admin,
                actor=report.reporter,
                report=report,
                notification_type='report',
                message=f"🚩 Nouveau signalement: {report.get_reason_display()} (par {reporter_name})"
            )
            logger.info(f"Notification créée pour {admin.username}: {notif.id}")
            
    except Exception as e:
        logger.error(f"Erreur lors de la création de notification admin: {str(e)}", exc_info=True)
