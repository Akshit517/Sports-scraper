from controllers.cricket_controller import CricketController
from scraper import Scraper


def main():
   # CricketController().run()
    scr = Scraper("Avesh khan")
    scr.start()


if __name__ == "__main__":
    main()
