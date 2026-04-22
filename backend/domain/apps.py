from django.apps import AppConfig


class DomainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domain'
    
    def ready(self):
        from .services import update_pending_songs
        import threading
        threading.Thread(target=update_pending_songs, daemon=True).start()
