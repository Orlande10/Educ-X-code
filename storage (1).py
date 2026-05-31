"""
storage.py
Handles reading from and writing to the local JSON data file.
"""

import json
import os

# Path to the data file used to persist quiz and user data
FILE: str = "data.json"


def read_data() -> dict:
    """
    Reads and returns the data stored in the JSON file.
    If the file does not exist yet, returns an empty dictionary.
    """
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data(data: dict) -> None:
    """
    Writes the given dictionary to the JSON file.
    Overwrites any existing content.
    """
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
