import json
import os


def count_events():

    ad_count_dict = {}

    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

    # get documents.json (../resorces/)
    with open("../resources/ad_counts.json", "r") as file:
        ad_count = json.load(file)

    for documents in json_files:
        with open(f"../data/{documents}", "r") as file:
            data = json.load(file)
        print(f"Processing {documents}")
        count = 1
        for result in data["results"]:
            if count % 1000 == 0:
                print(f"Processing result {count}")
            count += 1
            for drugs in result.get("patient", {}).get("drug", []):
                brandnames = sorted(drugs.get("openfda", {}).get("brand_name", []))
                if brandnames:
                    brandname = brandnames[0]
                    if brandname == "":
                        continue
                    if brandname not in ad_count:
                        ad_count_dict[brandname] = 1
                    else:
                        ad_count_dict[brandname] += 1
                    ad_count[brandname] = ad_count_dict[brandname]
            if count % 1000 == 0:
                with open("../resources/ad_counts.json", "w") as file:
                    json.dump(ad_count, file, indent=4)

    return None


if __name__ == "__main__":
    count_events()
