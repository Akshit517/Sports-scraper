import os

class Config:
    # Base URLs
    BASE_URL = "https://www.espncricinfo.com"
    LIVE_MATCHES_URL = "https://www.espncricinfo.com/live-cricket-score"
    
    # Output paths
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    CSV_OUTPUT_PATH = os.path.join(DATA_DIR, "live_scores.csv")
    
    # Request headers
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    # Scraping settings
    REQUEST_DELAY = 2  # seconds
    HEADLESS = True
    
    def __init__(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)