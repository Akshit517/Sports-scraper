from controllers.cricket_controller import CricketController
from scraper import Scraper
from scraper import Commentary


def main():
   # CricketController().run()
    scr = Scraper("Avesh khan")
    scr.start()

    cmntry = Commentary("115167")
    cmntry.get_commentary()


if __name__ == "__main__":
    main()
