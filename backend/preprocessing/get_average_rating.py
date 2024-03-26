import json
import pandas
from tqdm import tqdm

# tsv to df

df = pandas.read_csv("../data/drugsComTrain_raw.tsv", sep="\t")
df = df.dropna(subset=["review"])

ratings = {}
with open("brand_to_generic.json", "r") as file:
    brand_to_generic = json.load(file)
total_brands = len(brand_to_generic)
rows = df.iterrows()
count = 0
for i in tqdm(range(len(df))):
    count += 1
    for brand in brand_to_generic:
        # print("Processing brand name:", brand)
        for generic in brand_to_generic[brand]:
            # print("Processing generic name:", generic)

            if generic.lower() in df.loc[i, "drugName"].lower():
                # if generic.lower() == "acetaminophen":
                #     print(brand)
                ratings[brand] = ratings.get(brand, []) + [float(df.loc[i, "rating"])]
    if count % 10000 == 0:
        with open("ratings.json", "w") as file:
            json.dump(ratings, file, indent=4)
#         # if count % 10000 == 0:
#     print("Processed", count, "rows")

with open("ratings.json", "r") as file:
    ratings = json.load(file)
average_ratings = {}
for brand in ratings:
    average_ratings[brand] = sum(ratings[brand]) / len(ratings[brand])

with open("average_ratings.json", "w") as file:
    json.dump(average_ratings, file, indent=4)

# with open("average_ratings.json", "r") as file:
#     average_ratings = json.load(file)


# def round_average_ratings():
#     for brand in average_ratings:
#         average_ratings[brand] = round(average_ratings[brand], 1)
#     with open("average_ratings.json", "w") as file:
#         json.dump(average_ratings, file, indent=4)


# round_average_ratings()