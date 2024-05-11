import numpy as np
import pickle
import json
import os


abspath = os.path.abspath(__file__)

svd_path = os.path.join(os.path.dirname(abspath), "svd.sav")
index_to_json_path = os.path.join(os.path.dirname(abspath), "index_to_doc.json")
vectorizer_path = os.path.join(os.path.dirname(abspath), "vectorizer.sav")
tfidf_matrix = np.load(os.path.join(os.path.dirname(abspath), "tfidf_matrix.npy"))


def rocchio(query, relevant_docs, non_relevant_docs, alpha=1, beta=0.75, gamma=0.15):

    with open(index_to_json_path) as file:
        index_to_doc = json.load(file)
    doc_to_index = {v: k for k, v in index_to_doc.items()}
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    query_vec = vectorizer.transform([query]).toarray()

    relevant_doc_matrix = None

    for brand_name in relevant_docs:
        doc_id = int(doc_to_index[brand_name])
        doc_vec = tfidf_matrix[doc_id]
        if relevant_doc_matrix is None:
            relevant_doc_matrix = doc_vec
        else:
            relevant_doc_matrix = np.vstack([relevant_doc_matrix, doc_vec])

    non_relevant_doc_matrix = None

    for brand_name in non_relevant_docs:
        doc_id = int(doc_to_index[brand_name])
        doc_vec = tfidf_matrix[doc_id]
        if non_relevant_doc_matrix is None:
            non_relevant_doc_matrix = doc_vec
        else:
            non_relevant_doc_matrix = np.vstack([non_relevant_doc_matrix, doc_vec])
    if non_relevant_doc_matrix is None:
        non_relevant_mean = np.zeros_like(query_vec)
    else:
        non_relevant_mean = np.mean(non_relevant_doc_matrix, axis=0)

    if relevant_doc_matrix is None:
        relevant_mean = np.zeros_like(query_vec)
    else:
        relevant_mean = np.mean(relevant_doc_matrix, axis=0)
    new_query_vec = alpha * query_vec + beta * relevant_mean - gamma * non_relevant_mean

    return new_query_vec
