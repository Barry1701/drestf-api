from django.apps import AppConfig

class InboxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inbox"

    def ready(self):
        # to spowoduje zarejestrowanie sygnałów przy starcie Django
        import inbox.signals  # noqa
