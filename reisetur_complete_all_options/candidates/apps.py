from django.apps import AppConfig
class CandidatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'candidates'

    def ready(self):
        # import signals
        try:
            from . import signals  # noqa
        except Exception:
            pass
