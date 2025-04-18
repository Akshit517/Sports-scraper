from controllers.cricket_controller import CricketController
from miscellaneous import Scraper
from miscellaneous import Commentary
from multiprocessing import Process


def run_cricket_cotroller():
    CricketController().run()

# def run_commentary_controller():
#     CommentaryController("ipl-2025","1449924","115167","mumbai-indians-vs-sunrisers-hyderabad-33rd-match").run()

def run_scraper():
    # scraper = Scraper("Sachin Tendulkar")
    # scraper.start()
    pass
    
def main():
    p1 = Process(target=run_cricket_cotroller)
    # p2 = Process(target=run_commentary_controller)
    # p3 = Process(target=run_scraper)

    p1.start()
    # p2.start()
    # p3.start()

    p1.join()
    # p2.join()
    # p3.join()


if __name__ == "__main__":
    main()
