import pandas as pd

df = pd.read_json("security_events.jsonl", lines=True)

print(f"Total events logged: {len(df)}\n")

print("=== Impersonation attempts ===")
impersonation = df[df["event_type"] == "impersonation_attempt"]
if len(impersonation) > 0:
    for _, row in impersonation.iterrows():
        print(f"  {row['timestamp']}: claimed sender = {row['details']['claimed_sender']}, role = {row['details']['role']}")
else:
    print("  None detected.")

print("\n=== Denied tool calls by role ===")
denied = df[df["event_type"] == "tool_call_denied"]
if len(denied) > 0:
    denied_by_role = denied["details"].apply(lambda d: d["role"]).value_counts()
    print(denied_by_role)
else:
    print("  None detected.")