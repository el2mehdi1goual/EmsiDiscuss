"""
Configuration de l'application Accounts
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration de l'application Accounts
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Gestion des comptes'

    def ready(self):
        """
        Importe les signaux quand l'application est prête
        """
        import accounts.signals  # noqa
