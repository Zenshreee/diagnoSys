import json
import pandas as pd


def split_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    split = len(list(data.keys())) // 2

    for i in range(4):
        start = i * split
        end = (i + 1) * split
        if i == 3:
            end = len(list(data.keys()))
            try:
                name = json_file.split(".")[0]
            except:
                name = json_file
        with open(f"{name}_part{i+1}.json", "w") as file:
            json.dump(
                {key: data[key] for key in list(data.keys())[start:end]}, file, indent=4
            )

    return data


if __name__ == "__main__":
    split_json("drug_documents.json")
