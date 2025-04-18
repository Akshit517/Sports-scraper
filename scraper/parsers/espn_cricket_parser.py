from parsers.base_parser import BaseParser
from models.match_model import Match
import re
from datetime import datetime, timezone

class ESPNLiveCricketScoreParser(BaseParser):
    def parse(self) -> list[Match]:
        matches = []
        match_cards = self.soup.select("div.ds-px-4.ds-py-3")

        for card in match_cards:
            try:
                # Default IDs in case link is missing
                match_id = "unknown"
                series_id = "unknown"

                # Extract match/series ID from the link
                link_elem = card.select_one("a")
                if link_elem and link_elem.has_attr('href'):
                    match_url = link_elem['href']
                    match_id = self.extract_match_id(match_url)
                    series_id = self.extract_series_id(match_url)

                # Series name
                series_elem = card.find_previous("h2")
                series = series_elem.get_text(strip=True) if series_elem else "Unknown Series"

                # Teams
                team_names = card.select("p.ds-text-tight-m.ds-font-bold")
                if len(team_names) < 2:
                    continue
                team1 = team_names[0].get_text(strip=True)
                team2 = team_names[1].get_text(strip=True)

                # Scores
                scores = card.select("strong")
                score1 = scores[0].get_text(strip=True) if len(scores) > 0 else "N/A"
                score2 = scores[1].get_text(strip=True) if len(scores) > 1 else "N/A"

                # Overs
                overs = card.select("span.ds-text-compact-xs")
                over1 = overs[0].get_text(strip=True) if len(overs) > 0 else "N/A"
                over2 = overs[1].get_text(strip=True) if len(overs) > 1 else "N/A"

                # Status
                status_elem = card.select_one("p.ds-text-tight-s.ds-font-medium")
                status = status_elem.get_text(strip=True) if status_elem else "N/A"

                # Timestamp
                last_updated = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()  # Remove timezone info

                # Create Match object
                match = Match(
                    series,
                    team1,
                    team2,
                    over1,
                    over2,
                    score1,
                    score2,
                    status,
                    match_id,
                    series_id,
                    last_updated
                )
                matches.append(match)

            except Exception as e:
                print("Error parsing a match card:", e)
                continue

        return matches

    def extract_match_id(self, url: str) -> str:
        match = re.search(r'-(\d+)/(?:live-cricket-score|full-scorecard|match-schedule)', url)
        return match.group(1) if match else "unknown"

    def extract_series_id(self, url: str) -> str:
        match = re.search(r'/series/[^/]+-(\d+)', url)
        return match.group(1) if match else "unknown"
