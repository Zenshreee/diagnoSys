import numpy as np
import pickle
import json
from tfidf import tfidf_matrix


def rocchio(query, relevant_docs, non_relevant_docs, alpha=1, beta=0.75, gamma=0.15):
    vectorizer = pickle.load(open("vectorizer.sav", "rb"))
    query_vec = vectorizer.transform([query]).toarray()

    with open("index_to_doc.json") as file:
        index_to_doc = json.load(file)

    relevant_doc_matrix = None

    for brand_name in relevant_docs:
        doc_id = index_to_doc[brand_name]
        doc_vec = tfidf_matrix[doc_id]
        if relevant_doc_matrix is None:
            relevant_doc_matrix = doc_vec
        else:
            relevant_doc_matrix = np.vstack([relevant_doc_matrix, doc_vec])

    non_relevant_doc_matrix = None

    for brand_name in non_relevant_docs:
        doc_id = index_to_doc[brand_name]
        doc_vec = tfidf_matrix[doc_id]
        if non_relevant_doc_matrix is None:
            non_relevant_doc_matrix = doc_vec
        else:
            non_relevant_doc_matrix = np.vstack([non_relevant_doc_matrix, doc_vec])

    new_query_vec = (
        alpha * query_vec
        + beta * np.mean(relevant_doc_matrix, axis=0)
        - gamma * np.mean(non_relevant_doc_matrix, axis=0)
    )

    return new_query_vec
