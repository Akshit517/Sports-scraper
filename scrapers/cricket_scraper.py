from .base_scraper import BaseScraper

class CricketScraper(BaseScraper):
    def load_live_scores(self):
        self.navigate_to("https://www.espncricinfo.com/live-cricket-score")
        # Additional Selenium interactions if necessary
        return self.get_page_source()