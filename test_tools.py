from tools import create_ticket, read_asset_inventory, flag_for_human_review

print(create_ticket("Test ticket: laptop won't turn on"))
print(read_asset_inventory())
print(flag_for_human_review("Test escalation reason"))