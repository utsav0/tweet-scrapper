from django.apps import AppConfig
import os


class TweetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweets'

    def ready(self):
        from . import views

        if os.environ.get('RUN_MAIN', None) != 'true':
            views.start_scheduler()
