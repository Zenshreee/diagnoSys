import json
import pandas


print("making df")
df = pandas.read_csv("../data/combined_drug_reviews.tsv", sep="\t")
df = df.dropna(subset=["review"])
print("finishing df")

results = {}

for drug in df['drugName'].unique():
    drug_data = df[df['drugName'] == drug]
    
    top_reviews = drug_data.nlargest(2, 'rating')[['review', 'rating']]
    bottom_reviews = drug_data.nsmallest(2, 'rating')[['review', 'rating']]
    
    if len(top_reviews) >= 2:
        top_result = {
            'review1': top_reviews.iloc[0]['review'],
            'rating1': top_reviews.iloc[0]['rating'],
            'review2': top_reviews.iloc[1]['review'],
            'rating2': top_reviews.iloc[1]['rating']
        }
    else:
        top_result = {'review1': None, 'rating1': None, 'review2': None, 'rating2': None}
    
    if len(bottom_reviews) >= 2:
        bottom_result = {
            'review1': bottom_reviews.iloc[0]['review'],
            'rating1': bottom_reviews.iloc[0]['rating'],
            'review2': bottom_reviews.iloc[1]['review'],
            'rating2': bottom_reviews.iloc[1]['rating']
        }
    else:
        bottom_result = {'review1': None, 'rating1': None, 'review2': None, 'rating2': None}

    results[drug.lower()] = {
    'positive': top_result,
    'negative': bottom_result
    }


print("making json")
json_output = json.dumps(results, indent=4)


with open("reviews.json", "w") as file:
    json.dump(json_output, file, indent=4)
