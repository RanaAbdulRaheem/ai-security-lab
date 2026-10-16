import json, os

def create_ticket(description):
    tickets = json.load(open("tickets.json")) if os.path.exists("tickets.json") else []
    tickets.append({"description": description})
    json.dump(tickets, open("tickets.json", "w"))
    return f"Ticket created: {description}"

def read_asset_inventory():
    return open("./docs/asset_inventory.txt").read()

def flag_for_human_review(reason):
    with open("human_review_queue.txt", "a") as f:
        f.write(reason + "\n")
    return "Flagged for human review."