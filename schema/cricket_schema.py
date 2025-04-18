import pathway as pw

class CricketScores(pw.Schema):
    series: str
    team1: str
    team2: str
    over1: str
    over2: str
    score1: str
    score2: str
    status: str
    match_id: int
    series_id: int
    last_updated: pw.DateTimeNaive
