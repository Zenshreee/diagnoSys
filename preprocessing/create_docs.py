import json
import os

def process_documents():
    """
    Fetch definitions for each word in `reactionmeddrapt` entries.
    """
    drug_documents = {}

    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

    # get documents.json (../resorces/)
    with open("../resources/drug_documents.json", "r") as file:
        json_doc = json.load(file)

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
            for drugs in result.get("patient", {}).get("drug", []):
                brandname = ""
                brandnames = drugs.get("openfda", {}).get("brand_name",[])
                if brandnames:
                    brandname = brandnames[0]
                if brandname not in json_doc:
                    drug_documents[brandname] = ""
                if "generic_name" in drugs.get("openfda", {}):
                    genericname = drugs.get("openfda", {}).get("generic_name")
                    if genericname:
                        if genericname != brandname:
                            drug_documents[brandname]+=genericname[0]+" "
                for reaction in result.get("patient", {}).get("reaction", []):
                    reaction_phrase = reaction.get("reactionmeddrapt", "")
                    words = reaction_phrase.split()
                    for word in words:
                        word = word.lower()
                        if word in json_def:
                            drug_documents[brandname] += json_def[word] + " " + word
                if "patientonsetage" in result.get("patient", {}):
                    drug_documents[brandname] += " " + result.get("patient", {})["patientonsetage"]
            add_entry_to_json(drug_documents, "../resources/drug_documents.json")

    return drug_documents

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