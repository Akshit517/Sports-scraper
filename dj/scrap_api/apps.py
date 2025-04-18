from django.apps import AppConfig


class ScrapApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrap_api'

    def ready(self):
        from threading import Thread
        from django.core.management import call_command

        def run_scraping():
            call_command('start_commentary_scraping')

        thread = Thread(target=run_scraping, daemon=True)
        thread.start()
