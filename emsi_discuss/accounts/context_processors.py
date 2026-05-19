"""
Context processors pour l'application Accounts
"""


def user_ban_context(request):
    """Expose si l'utilisateur connecté est actuellement banni."""
    if request.user.is_authenticated:
        return {'user_is_banned': request.user.profile.is_currently_banned()}
    return {'user_is_banned': False}
