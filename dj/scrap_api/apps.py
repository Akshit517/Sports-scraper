from django.apps import AppConfig


class ScrapApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrap_api'

    def ready(self):
        # Call the management command when the app is ready (server starts)
        from threading import Thread
        from django.core.management import call_command

        def run_scraping():
            call_command('start_commentary_scraping')

        # Start scraping in a background thread
        thread = Thread(target=run_scraping, daemon=True)
        thread.start()
