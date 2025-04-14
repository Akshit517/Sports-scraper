from parsers.base_parser import BaseParser
from models.match_model import Match
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ESPNLiveCricketScoreParser(BaseParser):
    def parse(self) -> list[Match]:
        matches = []
        match_cards = self.soup.select("div.ds-px-4.ds-py-3")

        for card in match_cards:
            try:
                series_elem = card.find_previous("h2")
                series = series_elem.get_text(strip=True) if series_elem else "Unknown Series"

                team_names = card.select("p.ds-text-tight-m.ds-font-bold")
                if len(team_names) < 2:
                    continue

                team1 = team_names[0].get_text(strip=True)
                team2 = team_names[1].get_text(strip=True)

                scores = card.select("strong")
                score1 = scores[0].get_text(strip=True) if len(scores) > 0 else "N/A"
                score2 = scores[1].get_text(strip=True) if len(scores) > 1 else "N/A"

                overs = card.select("span.ds-text-compact-xs")
                over1 = overs[0].get_text(strip=True) if len(overs) > 0 else "N/A"
                over2 = overs[1].get_text(strip=True) if len(overs) > 1 else "N/A"

                status_elem = card.select_one("p.ds-text-tight-s.ds-font-medium")
                status = status_elem.get_text(strip=True) if status_elem else "N/A"

                match = Match(series, team1, team2, over1, over2, score1, score2, status)
                matches.append(match)

            except Exception as e:
                print("Error parsing a match card:", e)
                continue

        return matches
