from controllers.cricket_controller import CricketController
from scraper import Scraper


def main():
   # CricketController().run()
    scr = Scraper("virat kohli")
    scr.start()


if __name__ == "__main__":
    main()
