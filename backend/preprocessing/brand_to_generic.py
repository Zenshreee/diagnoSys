import json

import json
import os
import time


def brand_to_generic():
    """
    Fetch definitions for each word in `reactionmeddrapt` entries.
    """
    MAX = 1000
    MIN = 100
    brand_to_generic = {}
    num_added = {}
    files = os.listdir("../data")
    counter = 0
    json_files = [f for f in files if f.endswith(".json")]

    # get documents.json (../resorces/)
    with open("brand_to_generic.json", "r") as file:
        json_doc = json.load(file)

    # get definitions.json (../resorces/)
    # with open("definitions.json", "r") as file:
    #     json_def = json.load(file)

    # with open("ad_counts.json", "r") as file:
    #     ad_counts = json.load(file)

    # for key in ad_counts:
    #     num_added[key] = 0

    for documents in json_files:
        counter += 1
        # if counter >= 18:
        #     continue
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
                # if brandname in ad_counts:
                #     if ad_counts[brandname] < MIN or num_added[brandname] > MAX:
                #         continue
                if brandname == "":
                    continue
                if brandname not in json_doc:
                    brand_to_generic[brandname] = set()
                if "generic_name" in drugs.get("openfda", {}):
                    genericname = drugs.get("openfda", {}).get("generic_name")
                    if genericname:
                        for name in genericname:
                            brand_to_generic[brandname].add(name)

                json_doc[brandname] = list(brand_to_generic[brandname])
            if count % 1000 == 0:
                with open("brand_to_generic.json", "w") as file:
                    json.dump(json_doc, file, indent=4)
    return brand_to_generic


# def save_to_json(data, filename):
#     with open(filename, "w") as file:
#         json.dump(data, file, indent=4)


# """
# Add entry to json
# """


# def add_entry_to_json(data: dict, filename: str) -> None:
#     try:
#         with open(filename, "r") as file:
#             old_data = json.load(file)
#         old_data.update(data)
#         save_to_json(old_data, filename)
#     except:
#         print("didn't work")


if __name__ == "__main__":
    brand_to_generic()
