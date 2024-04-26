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
import time
import pickle
import os
import sys
import scipy as sp
from sklearn.decomposition import TruncatedSVD

# json_doc_file_path = "../resources/drug_documents.json"
# with open(json_doc_file_path, "r") as file:
#     documents = json.load(file)

# index_to_doc = {}
# for idx, doc in enumerate(list(documents.keys())):
#     index_to_doc[idx] = doc

# with open("../resources/index_to_doc.json", "w") as file:
#     json.dump(index_to_doc, file, indent=4)


# start = time.time()
# docs = list(documents.values())
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(docs)
# pickle.dump(vectorizer, open("vectorizer.sav", "wb"))
# tfidf_matrix = np.array(tfidf_matrix.toarray())
# end = time.time()
# print(f"Time taken to vectorize: {end - start}")
# np.save("../preprocessing/tfidf_matrix.npy", tfidf_matrix)

abspath = os.path.abspath(__file__)
filename = "tfidf_matrix.npy"
matrix_filepath = os.path.join(os.path.dirname(abspath), filename)
vectorizer_path = os.path.join(os.path.dirname(abspath), "vectorizer.sav")
index_to_json_path = os.path.join(os.path.dirname(abspath), "index_to_doc.json")
docspath = os.path.join(os.path.dirname(abspath), "drug_documents.json")
svd_path = os.path.join(os.path.dirname(abspath), "svd.sav")

drug_median_var_ages_path = os.path.join(
    os.path.dirname(abspath), "drug_median_var_ages.json"
)
# print python version
# print(sys.version)
# with open(docspath1, "r") as file:
#     documents_pt1 = json.load(file)
# with open(docspath2, "r") as file:
#     documents_pt2 = json.load(file)

# documents = {**documents_pt1, **documents_pt2}
with open(docspath, "r") as file:
    documents = json.load(file)

# index_to_doc = {}

# for idx, doc in enumerate(list(documents.keys())):
#     index_to_doc[idx] = doc

# with open(index_to_json_path, "w") as file:
#     json.dump(index_to_doc, file, indent=4)

# # # with open(vectorizer_path, "rb") as file:
# # #     vectorizer = pickle.load(file)
# vectorizer = TfidfVectorizer(stop_words="english")
# tfidf_matrix = vectorizer.fit_transform(list(documents.values()))
# pickle.dump(vectorizer, open(vectorizer_path, "wb"))
# tfidf_matrix = np.array(tfidf_matrix.toarray())
# np.save("tfidf_matrix.npy", tfidf_matrix)
# sp.sparse.save_npz("tfidf_matrix.npz", tfidf_matrix)
# tfidf_matrix = np.load(
#     os.path.join(os.path.dirname(abspath), filename), allow_pickle=True
# )

# tfidf_matrix = np.load(
#     os.path.join(os.path.dirname(abspath), "tfidf_matrix_svd.npy"), allow_pickle=True
# )

# svd = TruncatedSVD(n_components=40)
# tfidf_matrix = svd.fit_transform(tfidf_matrix)
# np.save("tfidf_matrix_svd.npy", tfidf_matrix)
# pickle.dump(svd, open("svd.sav", "wb"))

tfidf_matrix = np.load(os.path.join(os.path.dirname(abspath), "tfidf_matrix_svd.npy"))


# tfidf_matrix = sp.sparse.load_npz(matrix_filepath)
# print(np.array_equal(tfidf_matrix, laoded))
# cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[3:4])
# print(f"Cosine Similarity between the first and fourth documents: {cosine_sim[0][0]}")
# tfidf_matrix = np.load(matrix_filepath)


def query(tfidf_matrix, query):
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    input_vector = vectorizer.transform([query])
    input_vector = svd.transform(input_vector)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    for i, score in enumerate(cosine_similarities):
        document_name = index_to_doc[str(i)]
        # print(f"Cosine similarity with '{document_name}': {score}")

    top_10_indices = np.argsort(cosine_similarities)[::-1][:10]
    print("Top 10 most similar documents:")
    for index in top_10_indices:
        document_name = index_to_doc[str(index)]
        print(f"{document_name}: {cosine_similarities[index]}")


# start = time.time()
# query(
#     tfidf_matrix,
#     "I am a 20 year old and took albendazole, advil and xanax and now I have headache",
# )
# end = time.time()
# print(f"Time taken to query: {end - start}")


def query_with_age(tfidf_matrix, query, user_age):
    with open(drug_median_var_ages_path, "r") as file:
        ages = json.load(file)
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    input_vector = vectorizer.transform([query])
    input_vector = svd.transform(input_vector)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    # for i, score in enumerate(cosine_similarities):
    #     document_name = list(documents.keys())[i]
    #     print(f"Cosine similarity with '{document_name}': {score}")

    age_scores = cosine_similarities.copy()
    for i, score in enumerate(cosine_similarities):
        document_name = index_to_doc[str(i)]
        if document_name in ages:
            median_age = ages[document_name][0]
            std_dev = ages[document_name][1]
            multiplier = 1 + ((1 / ((abs(median_age - user_age) + 1) ** 2)))
            age_scores[i] = multiplier * score

    top_10_scores = np.argsort(cosine_similarities)[::-1][:10]

    accumualtor = []
    for i, doc_pos in enumerate(top_10_scores):
        document_name = index_to_doc[str(doc_pos)]
        if document_name in ages:
            median_age = ages[document_name][0]
            std_dev = ages[document_name][1]
            multiplier = 1 + (
                (1 / ((abs(median_age - user_age) + 1) ** 2))
            )  # 1+((1/(abs(median_age - user_age)+1)) * (1/(std_dev + 1)))
            accumualtor.append(multiplier)

    mean_multiplier = np.mean(accumualtor)

    for i, doc_pos in enumerate(top_10_scores):
        document_name = index_to_doc[str(doc_pos)]
        if document_name not in ages:
            age_scores[doc_pos] = age_scores[doc_pos] * mean_multiplier

    top_10_og_age_scores = [(age_scores[index], index) for index in top_10_scores]
    # top_10_age_scores = np.argsort(age_scores)[::-1][:10]
    rtrn_lst = []
    # print("Top 10 most similar documents:")
    for score, index in top_10_og_age_scores:
        document_name = index_to_doc[str(index)]
        rtrn_lst.append((document_name, score))
        # print(f"{document_name}: {score}")

    return rtrn_lst


# with open("average_ratings.json", "r") as file:
#     average_ratings = json.load(file)

# print(len(average_ratings))

# with open("ad_counts.json", "r") as file:
#     adcounts = json.load(file)

# print(len(adcounts))
# print()


# query_with_age(
#     tfidf_matrix,
#     "advil",
#     20,
# )
def print_top_terms_for_components(vectorizer, svd_model, n_top_terms=10):
    terms = vectorizer.get_feature_names_out()
    for i, comp in enumerate(svd_model.components_):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[
            :n_top_terms
        ]
        print(f"Component {i}:")
        for t in sorted_terms:
            print(f"{t[0]} ({t[1]:.2f})", end=" ")
        print("\n")


# Example usage
# vectorizer = pickle.load(open(vectorizer_path, "rb"))
# svd = pickle.load(open(svd_path, "rb"))
# print_top_terms_for_components(vectorizer, svd, n_top_terms=10)


def query_after_rocchio(tfidf_matrix, query_vec, user_age):
    user_age = float(user_age)

    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    with open(drug_median_var_ages_path, "r") as file:
        ages = json.load(file)
    with open(svd_path, "rb") as file:
        svd = pickle.load(file)
    input_vector = svd.transform(query_vec)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()
    age_scores = cosine_similarities.copy()
    for i, score in enumerate(cosine_similarities):
        document_name = index_to_doc[str(i)]
        if document_name in ages:
            median_age = ages[document_name][0]
            std_dev = ages[document_name][1]
            multiplier = 1 + ((1 / ((abs(median_age - user_age) + 1) ** 2)))
            age_scores[i] = multiplier * score

    top_10_scores = np.argsort(cosine_similarities)[::-1][:10]

    accumualtor = []
    for i, doc_pos in enumerate(top_10_scores):
        document_name = index_to_doc[str(doc_pos)]
        if document_name in ages:
            median_age = ages[document_name][0]
            std_dev = ages[document_name][1]
            multiplier = 1 + (
                (1 / ((abs(median_age - user_age) + 1) ** 2))
            )  # 1+((1/(abs(median_age - user_age)+1)) * (1/(std_dev + 1)))
            accumualtor.append(multiplier)

    mean_multiplier = np.mean(accumualtor)

    for i, doc_pos in enumerate(top_10_scores):
        document_name = index_to_doc[str(doc_pos)]
        if document_name not in ages:
            age_scores[doc_pos] = age_scores[doc_pos] * mean_multiplier

    top_10_og_age_scores = [(age_scores[index], index) for index in top_10_scores]
    # top_10_age_scores = np.argsort(age_scores)[::-1][:10]
    rtrn_lst = []
    # print("Top 10 most similar documents:")
    for score, index in top_10_og_age_scores:
        document_name = index_to_doc[str(index)]
        rtrn_lst.append((document_name, score))
        # print(f"{document_name}: {score}")

    return rtrn_lst


def query_with_explanation(query, tfidf_matrix, vectorizer, svd, top_k=10):
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)

    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    # Transform the query to the SVD-reduced space
    input_vector = vectorizer.transform([query])
    transformed_query = svd.transform(input_vector)

    # Calculate cosine similarity between the query and all documents
    cosine_similarities = cosine_similarity(transformed_query, tfidf_matrix).flatten()

    # Get the indices of the top K similar documents
    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]

    print("Top similar documents with explanations:")
    for index in top_indices:
        document_name = index_to_doc[str(index)]
        similarity_score = cosine_similarities[index]

        # Find top contributing components
        document_components = tfidf_matrix[
            index, :
        ]  # Component scores for the document
        query_components = transformed_query.flatten()  # Component scores for the query

        # Component contribution to the similarity score (dot product)
        contributions = document_components * query_components
        top_components = np.argsort(contributions)[::-1][
            :3
        ]  # Top 3 contributing components

        # Explain the influence of the top components
        explanation = ", ".join(
            [
                f"Component {i} (contribution: {contributions[i]:.2f})"
                for i in top_components
            ]
        )

        # Output the result with explanation
        print(
            f"{document_name}: Score {similarity_score:.3f}. Key components: {explanation}"
        )


# Example usage

# query_with_explanation(
#     "I'm taking flonase, triamcinolone, acetonide, cetirizine, montelukast sodium, symbicort, albuterol sulfate, epipen jr, fexofenadine hcl, levocetirizine dihydrochloride, mupirocin and I have asthma, allergic rhinitis, allergic conjuctivits, ezcema, acute uticaria. I am having difficulty breathing and rashes",
#     tfidf_matrix,
#     vectorizer,
#     svd,
#     top_k=10,
# )
