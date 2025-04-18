import os
import sys
scraper_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../../scraper'))
if scraper_path not in sys.path:
    sys.path.insert(0, scraper_path)

from commentry import Commentary
from live_match_scraper import LiveMatchStats
from django.core.management.base import BaseCommand
import threading
import time
class Command(BaseCommand):
    help = "Start scraping commentary data."

    
    def handle(self, *args, **kwargs):
        cooldown = 60  # seconds

        def run_scraping():
            codes = LiveMatchStats().scrap_codes()
            print(f"Scraping match codes: {codes}")

            for c in codes:
                threading.Thread(
                target=lambda: Commentary(c, cooldown).start_scraping(),
                daemon=True
                ).start()
                time.sleep(20)


        threading.Thread(target=run_scraping, daemon=True).start()
        self.stdout.write(self.style.SUCCESS("Started scraping commentary for all matches in the background."))

