"""
Script that deletes all json files in the data/ directory
"""

import os

def delete_files():
    # List all files in the data directory
    files = os.listdir("../resources")
    # Filter only the json files
    json_files = [f for f in files if f.endswith(".json")]
    # Delete each file
    for f in json_files:
        os.remove(f)
        print(f"Deleted {f}")
    

delete_files()