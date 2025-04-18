from controllers.cricket_controller import CricketController
from scraper import Scraper
from scraper import Commentary
from pathway_connector import Commentary_RAG


def main():
   # CricketController().run()
    # cmtry = CommentaryHandler()
    # cmtry.read_input("115167")
    # cmtry.run()
    # scr = Scraper("Avesh khan")
    # scr.start()

    # cmntry = Commentary("115167")
    # cmntry.get_commentary()
    Commentary_RAG().start_pipeline()


if __name__ == "__main__":
    main()
