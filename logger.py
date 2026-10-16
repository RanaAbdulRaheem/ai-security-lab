import json
from datetime import datetime

def log_event(event_type, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details
    }
    with open("security_events.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")