from connectors import BaseDriver
from pages import BasePage
from parsers import ESPNLiveCricketScoreParser
from exporters import CSVExporter

class CricketController:
    def __init__(self):
        self.browser = BaseDriver(binary_path="/snap/firefox/current/usr/lib/firefox/firefox")
        self.driver = self.browser.get_driver()

    def run(self):
        try:
            page = BasePage(self.driver)
            page.open_url("https://www.espncricinfo.com/live-cricket-score")

            html = self.browser.get_page_source()
            parser = ESPNLiveCricketScoreParser(html)
            matches = parser.parse()

            exporter = CSVExporter(filepath="data/live_scores.csv")
            exporter.export(matches)
        finally:
            self.browser.quit()
