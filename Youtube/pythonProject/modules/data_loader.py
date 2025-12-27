# modules/data_loader.py

import csv
import os
from modules.video_entry import VideoEntry

def load_dataset(path_value):
    """Load CSV manually without pandas; returns list of VideoEntry objects."""

    if not os.path.exists(path_value):
        print("File not found at given location.")
        return None

    loaded_list = []

    try:
        with open(path_value, "r", encoding="utf-8") as file_ref:
            reader = csv.DictReader(file_ref)
            for row in reader:
                loaded_list.append(VideoEntry(row))

        return loaded_list

    except Exception as err:
        print("Error loading dataset:", err)
        return None
