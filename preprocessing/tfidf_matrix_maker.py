import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle

json_doc_file_path = "../resources/drug_documents.json"
with open(json_doc_file_path, "r") as file:
    documents = json.load(file)

docs = list(documents.values())
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)
print(tfidf_matrix.shape)

np.save('../resources/tfidf_matrix',tfidf_matrix)