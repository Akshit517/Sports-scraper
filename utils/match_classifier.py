def classify_match_status(status: str) -> str:
    if not status or status == "N/A":
        return "unknown"
    if "won" in status.lower() or "match tied" in status.lower():
        return "finished"
    elif "yet to begin" in status.lower() or "starts in" in status.lower():
        return "upcoming"
    elif "day" in status.lower() and ("lead by" in status.lower() or "trail by" in status.lower()):
        return "live"  # Multi-day cricket matches
    else:
        return "live"