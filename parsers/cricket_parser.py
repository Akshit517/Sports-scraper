from .base_parser import BaseParser

class CricketParser(BaseParser):
    def extract_match_titles(self):
        match_cards = self.soup.find_all("div", class_="ds-px-4 ds-py-3")
        return [card.get_text(separator=" | ", strip=True) for card in match_cards]
