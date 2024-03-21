"""
Script to unzip files in data/ directory
"""

import zipfile
import os


def unzip_files():
    # List all files in the data directory
    files = os.listdir("../data")
    # Filter only the zip files
    zip_files = [f for f in files if f.endswith(".zip")]
    # Unzip each file
    for f in zip_files:
        with zipfile.ZipFile(f, "r") as file:
            file.extractall("../data")
            print(f"Unzipped {f}")


unzip_files()
