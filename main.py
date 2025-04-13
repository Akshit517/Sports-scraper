from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapers.cricket_scraper import CricketScraper
from parsers.cricket_parser import CricketParser

def main():
    options = Options()
    options.headless = True
    options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"

    driver = webdriver.Firefox(options=options)

    scraper = CricketScraper(driver)
    html_content = scraper.load_live_scores()
    parser = CricketParser(html_content)
    match_titles = parser.extract_match_titles()
    for title in match_titles:
        print(title)
        print("\n")
    scraper.close()

if __name__ == "__main__":
    main()
