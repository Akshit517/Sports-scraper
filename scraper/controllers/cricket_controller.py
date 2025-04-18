import time
from connectors import BaseDriver
from pages import BasePage
from parsers import ESPNLiveCricketScoreParser
from exporters import CSVExporter

class CricketController:
    def __init__(self, refresh_interval=10, run_duration=3000):
        self.refresh_interval = refresh_interval  # seconds between checks
        self.run_duration = run_duration          # total runtime in seconds
        self.browser = BaseDriver(binary_path="/snap/firefox/current/usr/lib/firefox/firefox")
        self.driver = self.browser.get_driver()
        self.exporter = CSVExporter(filepath="data/latest_scores.csv")

    def run(self):
        try:
            page = BasePage(self.driver)
            page.open_url("https://www.espncricinfo.com/live-cricket-score")

            start_time = time.time()

            while time.time() - start_time < self.run_duration:
                self.driver.refresh()
                time.sleep(2)  # Give time for content to reload

                html = self.browser.get_page_source()
                parser = ESPNLiveCricketScoreParser(html)
                matches = parser.parse()

                if self.exporter.has_changed(matches):
                    print("Data changed. Updating CSV...")
                    self.exporter.export(matches)
                else:
                    print("No change in data. Skipping update...")

                time.sleep(self.refresh_interval)

        finally:
            self.browser.quit()
