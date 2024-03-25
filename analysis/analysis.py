# import json
# import seaborn as sns
# import matplotlib.pyplot as plt
# from collections import Counter

# file_path = "../data/drug-event-0012-of-0035.json"
# with open(file_path, "r") as file:
#     data = json.load(file)


# drug_names = []
# print(len(data["results"]))
# for report in data["results"]:
#     if "drug" in report["patient"]:
#         for drug in report["patient"]["drug"]:
#             drug_name = drug.get("medicinalproduct", "Unknown")
#             drug_names.append(drug_name)

# print(len(set(drug_names)))

# file_path = "../data/drug-event-0014-of-0035.json"

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Sample documents
# documents = [
#     "The sky is blue and beautiful.",
#     "Love this blue and bright sky!",
#     "The quick brown fox jumps over the lazy dog.",
#     "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
#     "I love green eggs, ham, sausages, and bacon!",
#     "The brown fox is quick and the blue dog is lazy!",
#     "The sky is very blue and the sky is very beautiful today",
#     "The dog is lazy but the brown fox is quick!",
#     "The dog is lazy but the brown fox is!",
#     "The sky is blue and beautiful.",
#     "Love this blue and bright sky!",
#     "The quick brown fox jumps over the lazy dog.",
#     "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
#     "I love green eggs, ham, sausages, and bacon!",
#     "The brown fox is quick and the blue dog is lazy!",
#     "The sky is very blue and the sky is very beautiful today",
#     "The dog is lazy but the brown fox is quick!",
#     "The dog is lazy but the brown fox is!",
#     "The sky is blue and beautiful.",
#     "Love this blue and bright sky!",
#     "The quick brown fox jumps over the lazy dog.",
#     "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
#     "I love green eggs, ham, sausages, and bacon!",
#     "The brown fox is quick and the blue dog is lazy!",
#     "The sky is very blue and the sky is very beautiful today",
#     "The dog is lazy but the brown fox is quick!",
#     "The dog is lazy but the brown fox is!",
# ]

# # Your query
# query = ["The blue sky"]

# # Initialize the TfidfVectorizer
# tfidf_vectorizer = TfidfVectorizer()

# # Fit and transform the documents
# docs_tfidf = tfidf_vectorizer.fit_transform(documents)

# # Transform the query using the same vectorizer
# query_tfidf = tfidf_vectorizer.transform(query)

# # Compute the cosine similarity between query and all docs
# cosine_similarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()

# # Pair each document with its similarity score
# doc_similarity_pairs = [
#     (doc, score) for doc, score in zip(documents, cosine_similarities)
# ]

# # Sort the documents based on their similarity score in descending order
# sorted_doc_similarity_pairs = sorted(
#     doc_similarity_pairs, key=lambda x: x[1], reverse=True
# )

# # Display the sorted documents and their scores
# for doc, score in sorted_doc_similarity_pairs:
#     print(f"Score: {score:.4f}, Document: {doc}")

# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# df = pd.DataFrame(np.random.rand(40000, 40000))
# df["distances"] = cosine_similarity(
#     df, df.iloc[0:1]
# )  # Here I assume that the parent vector is stored as the first row in the dataframe, but you could also store it separately

# n = 10  # or however many you want
# n_largest = df["distances"].nlargest(
#     n + 1
# )  # this contains the parent itself as the most similar entry, hence n+1 to get n children
# print(n_largest)

# import json

# with open("../resources/drug_documents.json", "r") as file:
#     data = json.load(file)

# print(len(data))


