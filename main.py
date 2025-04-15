from controllers.cricket_controller import CricketController
from scraper import Scraper


def main():
   # CricketController().run()
    Scraper.start("Sachin Tendulkar")


if __name__ == "__main__":
    main()
