import pathway as pw
from schema.cricket_schema import CricketScores
from utils.match_classifier import classify_match_status
from transformers.live_insights import generate_insights

def run_pipeline():
    # Read the data from the CSV
    table = pw.io.csv.read("data/latest_scores.csv", schema=CricketScores, mode="streaming")
    
    # Add match status to the table
    table = table.with_columns(
        match_status=pw.apply(classify_match_status, table.status),
    )

    # Filter to get only live matches
    live_matches = table.filter(table.match_status == "live")
    
    # First, generate the insights as a structured column
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
    
    # Then extract the specific fields from the insights
    insights = with_raw_insights.with_columns(
        win_probability=pw.apply(lambda x: x["win_probability"] if x["win_probability"] is not None else 0.0, 
                              with_raw_insights.raw_insights),
        live_insight=pw.apply(lambda x: x["insight"], with_raw_insights.raw_insights)
    )

    # Select the necessary columns to output
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

    # Output the results
    pw.io.jsonlines.write(output, "./data/insights_output.json")
    
    # Run the pipeline
    pw.run()

if __name__ == "__main__":
    run_pipeline()
