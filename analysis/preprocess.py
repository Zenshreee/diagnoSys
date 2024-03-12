import json
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

file_path = '../data/drug-event-0014-of-0035.json'
with open(file_path, 'r') as file:
    data = json.load(file)

drug_names = []
for report in data['results']:
    if 'drug' in report['patient']:
        for drug in report['patient']['drug']:
            drug_name = drug.get('medicinalproduct', 'Unknown')
            drug_names.append(drug_name)

drug_counts = Counter(drug_names)

top_10_drugs = drug_counts.most_common(10)

drug_names, counts = zip(*top_10_drugs)
data_for_plot = {
    'Drug Name': drug_names,
    'Number of Reports': counts
}

import pandas as pd
df = pd.DataFrame(data_for_plot)

plt.figure(figsize=(10, 8))
sns.barplot(x='Number of Reports', y='Drug Name', data=df, palette='coolwarm')
plt.title('Top 10 Drugs by Number of Reports')

plt.savefig('top_10_drugs_report_seaborn.png')

plt.show()
