import re
from random import uniform
import pathway as pw

def parse_score(score: str):
    if not score or score == "N/A":
        return None, None
    
    # Handle scores with ampersand for multi-innings matches like "318&"
    score = score.split('&')[0] if '&' in score else score
    
    # Handle declared innings like "317/9d"
    score = score.replace('d', '') if 'd' in score else score
    
    match = re.match(r"(\d+)(/(\d+))?", score)
    if match:
        runs = int(match.group(1))
        wickets = int(match.group(3)) if match.group(3) else 0
        return runs, wickets
    return None, None

def extract_overs(over_str: str):
    if not over_str or over_str == "N/A":
        return None
    
    try:
        # Handle formats like "(18.1/20 ov, T:163)"
        match = re.search(r"\((\d+\.\d+)\/", over_str)
        if match:
            return float(match.group(1))
        
        # Handle formats like "(62 ov)"
        match = re.search(r"\((\d+(\.\d+)?)\s*ov\)", over_str)
        if match:
            return float(match.group(1))
        
        # Handle other potential formats
        match = re.search(r"(\d+(\.\d+)?)", over_str)
        if match:
            return float(match.group(1))
    except:
        pass
    
    return None

def is_test_match(series: str, status: str):
    """Determine if this is a test/multi-day match based on series name or status"""
    if "day" in status.lower():
        return True
    
    test_indicators = ["test", "county championship", "3-day", "4-day", "merwais nika regional"]
    return any(indicator in series.lower() for indicator in test_indicators)

def calculate_win_probability(series, status, score1, score2, over1, over2):
    # For multi-day matches, use a different calculation logic
    if is_test_match(series, status):
        try:
            # Extract lead information from status
            lead_match = re.search(r"lead by (\d+) runs", status)
            if lead_match:
                lead = int(lead_match.group(1))
                # Simple model for test matches - higher lead = higher win probability
                if "day 5" in status.lower() or "day 4" in status.lower():
                    # Late in the match, lead is more significant
                    win_prob = min(100, max(0, 50 + lead * 0.5))
                else:
                    # Earlier in the match, lead is less decisive
                    win_prob = min(100, max(0, 50 + lead * 0.2))
                return round(win_prob, 2)
        except:
            return None
        
        return None
    
    # T20/ODI match calculation
    try:
        runs1, _ = parse_score(score1)
        runs2, _ = parse_score(score2)
        
        if runs1 is None or runs2 is None:
            return None
            
        overs_completed = extract_overs(over2)
        if overs_completed is None or overs_completed == 0:
            return None
            
        target = runs1 + 1
        current_rr = runs2 / overs_completed
        
        # Assuming T20 match (20 overs) by default
        total_overs = 20
        if "odi" in series.lower():
            total_overs = 50
            
        remaining_overs = total_overs - overs_completed
        if remaining_overs <= 0:
            # Match is about to end
            if runs2 >= target:
                return 100.0  # Batting team will win
            else:
                return 0.0    # Batting team will lose
                
        required_rr = (target - runs2) / remaining_overs
        
        # Basic win probability model
        win_prob = max(0, min(1, 0.5 + 0.05 * (current_rr - required_rr)))
        return round(win_prob * 100, 2)
    except Exception as e:
        return None

def generate_insights(match_id, series, team1, team2, score1, score2, over1, over2, status):
    win_prob = None
    insight = "Insufficient data for prediction."
    
    # Only calculate if we have sufficient data
    if score1 and score1 != "N/A" and score2 and score2 != "N/A":
        try:
            if is_test_match(series, status):
                # For test/multi-day matches
                win_prob = calculate_win_probability(series, status, score1, score2, over1, over2)
                if win_prob is not None:
                    # Extract which team is leading from the status
                    leading_team = None
                    if "lead by" in status:
                        if team1.lower() in status.lower():
                            leading_team = team1
                        elif team2.lower() in status.lower():
                            leading_team = team2
                    
                    if leading_team:
                        insight = f"{leading_team} has a {win_prob:.2f}% chance of winning based on current lead"
            else:
                # For limited overs matches
                win_prob = calculate_win_probability(series, status, score1, score2, over1, over2)
                if win_prob is not None:
                    insight = (
                        f"Live match between {team1} and {team2}. "
                        f"Win probability for {team2}: {win_prob:.2f}%"
                    )
        except Exception as e:
            pass
    
    return {"win_probability": win_prob, "insight": insight}
