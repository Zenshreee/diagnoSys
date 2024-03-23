import json
import os
import time


def process_documents():
    """
    Fetch definitions for each word in `reactionmeddrapt` entries.
    """
    MAX = 1000
    MIN = 100
    drug_documents = {}
    num_added = {}
    files = os.listdir("../data")
    counter = 0
    json_files = [f for f in files if f.endswith(".json")]

    # get documents.json (../resorces/)
    with open("drug_documents.json", "r") as file:
        json_doc = json.load(file)

    # get definitions.json (../resorces/)
    with open("definitions.json", "r") as file:
        json_def = json.load(file)

    with open("ad_counts.json", "r") as file:
        ad_counts = json.load(file)

    for key in ad_counts:
        num_added[key] = 0

    for documents in json_files:
        counter += 1
        if counter >= 18:
            continue
        print(f"Processing {documents}")
        with open(f"../data/{documents}", "r") as file:
            try:
                data = json.load(file)
            except:
                print(f"Error processing {documents}")
                continue
        # print(f"Processing {documents}")
        count = 1
        for result in data["results"]:
            if count % 1000 == 0:
                print(f"Processing result {count}")
            count += 1
            for drugs in result.get("patient", {}).get("drug", []):
                brandname = ""
                brandnames = sorted(drugs.get("openfda", {}).get("brand_name", []))
                if brandnames:
                    brandname = brandnames[0]
                if brandname in ad_counts:
                    if ad_counts[brandname] < MIN or num_added[brandname] > MAX:
                        continue
                if brandname == "":
                    continue
                if brandname not in json_doc:
                    drug_documents[brandname] = brandname.lower() + " "
                else:
                    drug_documents[brandname] = brandname.lower() + " "
                if "generic_name" in drugs.get("openfda", {}):
                    genericname = drugs.get("openfda", {}).get("generic_name")
                    if genericname:
                        for name in genericname:
                            if genericname != brandname:
                                drug_documents[brandname] += name.lower() + " "
                for reaction in result.get("patient", {}).get("reaction", []):
                    reaction_phrase = reaction.get("reactionmeddrapt", "")
                    drug_documents[brandname] += reaction_phrase + " "
                    words = reaction_phrase.split()
                    for word in words:
                        word = word.lower()
                        if word in json_def:
                            drug_documents[brandname] += json_def[word] + " "
                if "patientonsetage" in result.get("patient", {}):
                    if result.get("patient", {})["patientonsetage"]:
                        drug_documents[brandname] += (
                            " " + result.get("patient", {})["patientonsetage"]
                        ) + " "
                if "patientsex" in result.get("patient", {}):
                    patientsex = result.get("patient", {})["patientsex"]
                    if patientsex:
                        if patientsex == "1":
                            drug_documents[brandname] += " " + "male" + " "
                        elif patientsex == "2":
                            drug_documents[brandname] += " " + "female" + " "
                if brandname in json_doc:
                    json_doc[brandname] += drug_documents[brandname]
                    num_added[brandname] += 1
                else:
                    json_doc[brandname] = drug_documents[brandname]
                    num_added[brandname] = 1
            if count % 1000 == 0:
                with open("drug_documents.json", "w") as file:
                    json.dump(json_doc, file, indent=4)
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
