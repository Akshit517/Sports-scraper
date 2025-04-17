from controllers.cricket_controller import CricketController
from scraper import Scraper
from commentary_scraper.live_match_stats import LiveMatchStats


def main():   
    
    stats=LiveMatchStats()
    stats.get_Stats()
    

if __name__ == "__main__":
    main()
