import json
import os

FILE = "data.json" 

def read_data():
    if not os.path.exists(FILE):
        return {}
    
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
    def write_data(data):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent= 4 , ensure_ascii=False)