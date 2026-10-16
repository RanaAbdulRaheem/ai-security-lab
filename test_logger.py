from logger import log_event

log_event("test_event", {"message": "logger is working"})
print("Logged one test event. Check security_events.jsonl")