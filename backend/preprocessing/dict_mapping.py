import requests
import json
import os
from dotenv import load_dotenv
import time
import typing

load_dotenv()

api_key = os.getenv("API_KEY")

endpoint = (
    "https://www.dictionaryapi.com/api/v3/references/medical/json/{word}?key={api_key}"
)


def query_merriam_webster(word):
    """
    Querying Merriam-Webster API for a given medical term and returning the definition.
    """
    response = requests.get(endpoint.format(word=word, api_key=api_key))
    if response.status_code == 200:
        try:
            data = response.json()
            # taking only first definition
            if data and type(data[0]) != str:
                res = data[0].get("shortdef", [[]])
                if res:
                    return res[0]
        except:
            print(f"Error processing {word}")
    return []


def process_documents():
    """
    Fetch definitions for each word in `reactionmeddrapt` entries.
    """
    definitions = {}

    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

    # get definitions.json (../resorces/)
    with open("../resources/definitions.json", "r") as file:
        json_def = json.load(file)

    for documents in json_files:
        with open(f"../data/{documents}", "r") as file:
            data = json.load(file)
        print(f"Processing {documents}")
        count = 1
        for result in data["results"]:
            if count % 100 == 0:
                print(f"Processing result {count}")
            count += 1
            for reaction in result.get("patient", {}).get("reaction", []):
                reaction_phrase = reaction.get("reactionmeddrapt", "")
                words = reaction_phrase.split()
                for word in words:
                    word = word.lower()
                    if word not in json_def:
                        if (
                            word not in definitions
                        ):  # Avoid repeating API calls for the same word
                            defin = query_merriam_webster(word)
                            if defin:
                                definitions[word] = defin
                                add_entry_to_json(
                                    definitions, "../resources/definitions.json"
                                )
                            time.sleep(0.5)

    return definitions


# save to json file
def save_to_json(data, filename):

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


"""
Add entry to json
"""


def add_entry_to_json(data: dict, filename: str) -> None:
    try:
        with open(filename, "r") as file:
            old_data = json.load(file)
        old_data.update(data)
        save_to_json(old_data, filename)
    except:
        print("didn't work")


if __name__ == "__main__":
    process_documents()
