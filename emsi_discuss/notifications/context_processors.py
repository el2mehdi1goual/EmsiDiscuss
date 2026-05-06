"""
Context processor pour les notifications
"""
from notifications.models import Notification


def notifications_context(request):
    """
    Ajoute les informations de notifications au contexte global
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        unread_count = 0
    
    return {
        'unread_notifications_count': unread_count,
    }
