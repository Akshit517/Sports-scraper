from dataclasses import dataclass
from datetime import datetime

@dataclass
class Match:
    series: str
    team1: str
    team2: str
    over1: str
    over2: str
    score1: str
    score2: str
    status: str
    match_id: str
    series_id: str
    last_updated: datetime
