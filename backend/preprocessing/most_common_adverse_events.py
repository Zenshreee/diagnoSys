import json
import os

with open("most_common_ad_events.json", "r") as file:
    ad_events = json.load(file)

list_of_words = set(["device", "drug", "wrong", "product", "dose"])


def get_most_common_ad_events():

    ad_events = {}
    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

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
                    if brandname not in ad_events:
                        ad_events[brandname] = {}
                    for reaction in result.get("patient", {}).get("reaction", []):
                        reaction_phrase = reaction.get("reactionmeddrapt", "")
                        lower_reaction_phrase = reaction_phrase.lower()
                        flag = False
                        for word in list_of_words:
                            if word in lower_reaction_phrase:
                                flag = True
                        if flag:
                            continue
                        if reaction_phrase not in ad_events[brandname]:
                            ad_events[brandname][reaction_phrase] = 1
                        else:
                            ad_events[brandname][reaction_phrase] += 1

    counts = {}
    for brand in ad_events:
        counts[brand] = sorted(
            ad_events[brand].items(), key=lambda x: x[1], reverse=True
        )[:5]

    with open("most_common_ad_events.json", "w") as file:
        json.dump(counts, file, indent=4)

    return None


if __name__ == "__main__":
    get_most_common_ad_events()
