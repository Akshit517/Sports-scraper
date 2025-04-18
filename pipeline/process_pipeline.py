import pathway as pw
from schema.cricket_schema import CricketScores
from utils.match_classifier import classify_match_status
from transformers.live_insights import generate_insights

def run_pipeline():
    table = pw.io.csv.read("data/latest_scores.csv", schema=CricketScores, mode="streaming")
    
    table = table.with_columns(
        match_status=pw.apply(classify_match_status, table.status),
    )

    live_matches = table.filter(table.match_status == "live")
    
    with_raw_insights = live_matches.with_columns(
        raw_insights=pw.apply(
            generate_insights,
            live_matches.match_id,
            live_matches.series,
            live_matches.team1,
            live_matches.team2,
            live_matches.score1,
            live_matches.score2,
            live_matches.over1,
            live_matches.over2,
            live_matches.status
        )
    )
    
    insights = with_raw_insights.with_columns(
        win_probability=pw.apply(lambda x: x["win_probability"] if x["win_probability"] is not None else 0.0, 
                              with_raw_insights.raw_insights),
        live_insight=pw.apply(lambda x: x["insight"], with_raw_insights.raw_insights)
    )

    output = insights.select(
        insights.match_id,
        insights.series,
        insights.team1,
        insights.team2,
        insights.score1,
        insights.score2,
        insights.over1,
        insights.over2,
        insights.status,
        insights.win_probability,
        insights.live_insight,
    )

    pw.io.jsonlines.write(output, "./data/insights_output.jsonl")
    
    pw.run()

if __name__ == "__main__":
    run_pipeline()
