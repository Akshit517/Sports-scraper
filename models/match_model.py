from dataclasses import dataclass

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
