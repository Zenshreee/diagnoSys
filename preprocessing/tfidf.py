# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from scipy.sparse import csr_matrix
# import mysql.connector

# conn = mysql.connector.connect(
#     host="localhost",
#     user="",
#     password="",
#     database="definitions_db"
# )

# cursor = conn.cursor()

# query = 'SELECT * FROM definitions'

# cursor.execute(query)

# # for row in cursor.fetchall():

# conn.close()



# def json_to_tfidf(path: str) -> csr_matrix:
#     with open(path, "r") as file:
#         adverse_to_webster = json.load(file)

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math

json_doc_file_path = '../resources/drug_documents.json'
with open(json_doc_file_path, 'r') as file:
    documents = json.load(file)

json_age_file_path = '../resources/drug_median_var_ages.json'
with open(json_age_file_path, 'r') as file:
    ages = json.load(file)

docs = list(documents.values())
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[3:4])
print(f"Cosine Similarity between the first and fourth documents: {cosine_sim[0][0]}")

def query(tfidf_matrix, query):
    input_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    for i, score in enumerate(cosine_similarities):
        document_name = list(documents.keys())[i]
        # print(f"Cosine similarity with '{document_name}': {score}")

    top_10_indices = np.argsort(cosine_similarities)[::-1][:10]
    print("Top 10 most similar documents:")
    for index in top_10_indices:
        document_name = list(documents.keys())[index] 
        print(f"{document_name}: {cosine_similarities[index]}")

query(tfidf_matrix, "I am a 20 year old and took albendazole, advil and xanax and now I have headache")


def query_with_age(tfidf_matrix, query, user_age):
    input_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    # for i, score in enumerate(cosine_similarities):
    #     document_name = list(documents.keys())[i]
    #     print(f"Cosine similarity with '{document_name}': {score}")

    age_scores = cosine_similarities.copy()
    for i, score in enumerate(cosine_similarities):
        document_name = list(documents.keys())[i]
        if document_name in ages:
            median_age = ages[document_name][0]
            std_dev = ages[document_name][1]
            multiplier = 1+((1/(abs(median_age - user_age)+1))*(1/(std_dev+1)))
            age_scores[i] = multiplier * score

    # top_10_scores = np.argsort(cosine_similarities)[::-1][:10]

    # accumualtor = []
    # for i, doc_pos in enumerate(top_10_scores):
    #     document_name = list(documents.keys())[doc_pos]
    #     if document_name in ages:
    #         accumualtor.append(age_scores[doc_pos])
        
    # mean_multiplier = np.mean(accumualtor)
    
    # for i, doc_pos in enumerate(top_10_scores):
    #     document_name = list(documents.keys())[doc_pos]
    #     if document_name not in ages:
    #         age_scores[doc_pos] = age_scores[doc_pos] * mean_multiplier

    top_10_age_scores = np.argsort(age_scores)[::-1][:10]
    print("Top 10 most similar documents:")
    for index in top_10_age_scores:
        document_name = list(documents.keys())[index] 
        print(f"{document_name}: {age_scores[index]}")

print()
query_with_age(tfidf_matrix, "I am a 20 year old and took albendazole, advil and xanax and now I have headache", 60)
