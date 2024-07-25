import os
from RPA.Robocorp.WorkItems import WorkItems


search_phrase = "Tennis"
no_of_months = 1
if os.getenv("ENVIRONMENT") == "PROD":
    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_payload()
    search_phrase = work_item.get("search_phrase")
    no_of_months = work_item.get("no_of_months")
