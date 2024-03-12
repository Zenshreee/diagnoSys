import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
with open("../data/drug-event-0014-of-0035.json", "r") as f:
    data = json.load(f)["results"]

# Process data
drug_death_counts = {}
for entry in data:
    if entry.get("seriousnessdeath") == "1":  # Check if the death flag is set
        drugs = entry.get("patient", {}).get("drug", [])
        for drug in drugs:
            drug_name = drug.get("medicinalproduct")
            if drug_name:  # Check if drug name exists
                drug_death_counts[drug_name] = drug_death_counts.get(drug_name, 0) + 1

# Create DataFrame
drug_death_df = pd.DataFrame(
    list(drug_death_counts.items()), columns=["Drug", "DeathCount"]
)

# Sort and get top 10
top_10_drug_deaths = drug_death_df.sort_values("DeathCount", ascending=False).head(10)

# Plot using Seaborn
plt.figure(figsize=(14, 7))
sns.barplot(x="Drug", y="DeathCount", data=top_10_drug_deaths)
plt.title("Top 10 Drugs by Seriousness Death Reports")
plt.xlabel("Drug Name")
plt.ylabel("Death Count")
plt.xticks(rotation=90)
plt.tight_layout()  # Adjust the padding between and around subplots


plt.savefig("top_10_drugs_by_death_occurence.png")

plt.show()
