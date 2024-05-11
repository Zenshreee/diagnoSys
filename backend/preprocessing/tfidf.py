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


abspath = os.path.abspath(__file__)
filename = "tfidf_matrix.npy"
matrix_filepath = os.path.join(os.path.dirname(abspath), filename)
vectorizer_path = os.path.join(os.path.dirname(abspath), "vectorizer.sav")
index_to_json_path = os.path.join(os.path.dirname(abspath), "index_to_doc.json")
docspath = os.path.join(os.path.dirname(abspath), "drug_documents.json")
svd_path = os.path.join(os.path.dirname(abspath), "svd.sav")
components_path = os.path.join(os.path.dirname(abspath), "components.json")

drug_median_var_ages_path = os.path.join(
    os.path.dirname(abspath), "drug_median_var_ages.json"
)
with open(docspath, "r") as file:
    documents = json.load(file)

tfidf_matrix = np.load(os.path.join(os.path.dirname(abspath), "tfidf_matrix_svd.npy"))

old_tfidf_matrix = np.load(
    os.path.join(os.path.dirname(abspath), "tfidf_matrix.npy"), allow_pickle=True
)


def query(tfidf_matrix, query):
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    input_vector = vectorizer.transform([query])
    input_vector_old = input_vector
    input_vector = svd.transform(input_vector)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    cosine_similarities_old = cosine_similarity(input_vector_old, old_tfidf_matrix)
    cosine_similarities_old = cosine_similarities_old.flatten()

    interpolated_similarities = (
        0.5 * cosine_similarities + 0.5 * cosine_similarities_old
    )

    for i, score in enumerate(cosine_similarities):
        document_name = index_to_doc[str(i)]

    top_10_indices = np.argsort(cosine_similarities)[::-1][:10]
    print("Top 10 most similar documents:")
    for index in top_10_indices:
        document_name = index_to_doc[str(index)]
        print(f"{document_name}: {cosine_similarities[index]}")


def query_with_age(tfidf_matrix, query, user_age, svd_weight=0.3, cos_weight=0.7):
    with open(components_path, "r") as file:
        components = json.load(file)
    with open(drug_median_var_ages_path, "r") as file:
        ages = json.load(file)
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    input_vector = vectorizer.transform([query])
    input_vector_old = input_vector
    input_vector = svd.transform(input_vector)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    cosine_similarities_old = cosine_similarity(input_vector_old, old_tfidf_matrix)
    cosine_similarities_old = cosine_similarities_old.flatten()

    interpolated_similarities = (
        svd_weight * cosine_similarities + cos_weight * cosine_similarities_old
    )

    cosine_similarities = interpolated_similarities

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
            multiplier = 1 + ((1 / ((abs(median_age - user_age) + 1) ** 2)))
            accumualtor.append(multiplier)

    mean_multiplier = np.mean(accumualtor)

    for i, doc_pos in enumerate(top_10_scores):
        document_name = index_to_doc[str(doc_pos)]
        if document_name not in ages:
            age_scores[doc_pos] = age_scores[doc_pos] * mean_multiplier

    top_10_og_age_scores = [(age_scores[index], index) for index in top_10_scores]

    top_10_og_age_scores = sorted(
        top_10_og_age_scores, key=lambda x: x[0], reverse=True
    )

    rtrn_lst = []
    for score, index in top_10_og_age_scores:
        document_name = index_to_doc[str(index)]
        adding = (document_name, score)

        rtrn_lst.append(adding)
    rtrn_lst = sorted(rtrn_lst, key=lambda x: x[1], reverse=True)

    query_components = input_vector.flatten()
    top_indices = np.argsort(cosine_similarities)[::-1][:10]

    top_components_per_drug = []
    for index in top_indices:
        document_name = index_to_doc[str(index)]
        document_components = tfidf_matrix[index, :]

        contributions = document_components * query_components
        top_components = np.argsort(contributions)[::-1][:3]
        component_names = []
        component_score = []
        for comp in top_components:
            component_names.append(components[str(comp)])
            component_score.append(contributions[comp])
        total = sum(component_score)

        if total == 0:
            total = 1
        component_scores_100 = [
            round((score / total) * 100, 2) for score in component_score
        ]
        top_components_per_drug.append(
            (document_name, component_names, component_scores_100)
        )

    total_score = sum([score for _, score in rtrn_lst])
    if total_score == 0:
        total_score = 1
    return_list = []
    for i in range(len(rtrn_lst)):
        drug = rtrn_lst[i][0]
        score = round((rtrn_lst[i][1] / total_score) * 100, 2)
        top_components = top_components_per_drug[i]
        component_1 = top_components[1][0]
        component_2 = top_components[1][1]
        component_3 = top_components[1][2]
        component_score_1 = top_components[2][0]
        component_score_2 = top_components[2][1]
        component_score_3 = top_components[2][2]
        return_list.append(
            (
                drug,
                score,
                component_1,
                component_score_1,
                component_2,
                component_score_2,
                component_3,
                component_score_3,
            )
        )

    return return_list


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


def query_after_rocchio(
    tfidf_matrix, query_vec, user_age, svd_weight=0.3, cos_weight=0.7
):
    user_age = float(user_age)
    with open(components_path, "r") as file:
        components = json.load(file)
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)
    with open(drug_median_var_ages_path, "r") as file:
        ages = json.load(file)
    with open(svd_path, "rb") as file:
        svd = pickle.load(file)

    input_vector = svd.transform(query_vec)
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
    cosine_similarities = cosine_similarities.flatten()

    cosine_similarities_old = cosine_similarity(query_vec, old_tfidf_matrix)
    cosine_similarities_old = cosine_similarities_old.flatten()

    interpolated_similarities = (
        svd_weight * cosine_similarities + cos_weight * cosine_similarities_old
    )

    cosine_similarities = interpolated_similarities

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

    top_10_og_age_scores = sorted(
        top_10_og_age_scores, key=lambda x: x[0], reverse=True
    )

    rtrn_lst = []

    for score, index in top_10_og_age_scores:
        document_name = index_to_doc[str(index)]
        rtrn_lst.append((document_name, score))

    query_components = input_vector.flatten()
    top_indices = np.argsort(cosine_similarities)[::-1][:10]

    top_components_per_drug = []
    for index in top_indices:
        document_name = index_to_doc[str(index)]
        document_components = tfidf_matrix[index, :]
        contributions = document_components * query_components
        top_components = np.argsort(contributions)[::-1][:3]
        component_names = []
        component_score = []
        for comp in top_components:
            component_names.append(components[str(comp)])
            component_score.append(input_vector.flatten()[comp])
        totals = sum(component_score)
        if totals == 0:
            totals = 1

        component_scores_100 = [
            round((score / totals) * 100, 2) for score in component_score
        ]
        top_components_per_drug.append(
            (document_name, component_names, component_scores_100)
        )

    total_score = sum([score for _, score in rtrn_lst])
    if total_score == 0:
        total_score = 1
    return_list = []
    for i in range(len(rtrn_lst)):
        drug = rtrn_lst[i][0]
        score = rtrn_lst[i][1]
        score = round((score / total_score) * 100, 2)
        top_components = top_components_per_drug[i]
        component_1 = top_components[1][0]
        component_2 = top_components[1][1]
        component_3 = top_components[1][2]
        component_score_1 = top_components[2][0]
        component_score_2 = top_components[2][1]
        component_score_3 = top_components[2][2]
        return_list.append(
            (
                drug,
                score,
                component_1,
                component_score_1,
                component_2,
                component_score_2,
                component_3,
                component_score_3,
            )
        )

    return return_list


def query_with_explanation(query, tfidf_matrix, vectorizer, svd, top_k=10):
    with open(index_to_json_path, "r") as file:
        index_to_doc = json.load(file)

    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    svd = pickle.load(open(svd_path, "rb"))
    input_vector = vectorizer.transform([query])
    transformed_query = svd.transform(input_vector)

    cosine_similarities = cosine_similarity(transformed_query, tfidf_matrix).flatten()

    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]

    print("Top similar documents with explanations:")
    for index in top_indices:
        document_name = index_to_doc[str(index)]
        similarity_score = cosine_similarities[index]

        document_components = tfidf_matrix[index, :]
        query_components = transformed_query.flatten()

        contributions = document_components * query_components
        top_components = np.argsort(contributions)[::-1][:3]

        explanation = ", ".join(
            [
                f"Component {i} (contribution: {contributions[i]:.2f})"
                for i in top_components
            ]
        )
        print(
            f"{document_name}: Score {similarity_score:.3f}. Key components: {explanation}"
        )
