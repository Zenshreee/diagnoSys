import json
import os
from preprocessing.tfidf import tfidf_matrix, query_with_age, query_after_rocchio
from preprocessing.closest_drug import get_5_closest_drugs
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from preprocessing.rocchio import rocchio

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ["ROOT_PATH"] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = ""
LOCAL_MYSQL_PORT = 3306
LOCAL_MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(
    LOCAL_MYSQL_USER, LOCAL_MYSQL_USER_PASSWORD, LOCAL_MYSQL_PORT, LOCAL_MYSQL_DATABASE
)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)


# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this
def sql_search(episode):
    query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
    keys = ["id", "title", "descr"]
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys, i)) for i in data])


@app.route("/")
def home():
    return render_template("base.html", title="sample html")


def get_def(term):
    definitions_path = os.path.join(
        os.path.dirname(__file__), "preprocessing", "definitions.json"
    )
    with open(definitions_path, "r") as file:
        json_def = json.load(file)
    if term.lower() not in json_def:
        return ""
    return json_def[term.lower()]


def get_top_5_ad_events(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing", "most_common_ad_events.json")
    with open(datadir, "r") as file:
        top_5 = json.load(file)
    if drug_name not in top_5:
        return []
    res = []
    for i in top_5[drug_name][:5]:
        res.append([i[0]])
    return res


def get_rating(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing", "average_ratings.json")
    with open(datadir, "r") as file:
        ratings = json.load(file)
    if drug_name not in ratings:
        return "Rating not found"
    return ratings[drug_name]


def get_median_age(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing", "drug_median_var_ages.json")
    with open(datadir, "r") as file:
        median_ages = json.load(file)
    if drug_name not in median_ages:
        return "Not Found"
    return str(round(median_ages[drug_name][0], 1))


def get_usage(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing", "drug_use.json")
    with open(datadir, "r") as file:
        usage = json.load(file)
    if drug_name not in usage:
        return []
    res = []
    for i in usage[drug_name]:
        res.append([i])
    return res


def get_reviews(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing/reviews.json")
    with open(datadir, "r") as file:
        reviews = json.load(file)
    drug_name = drug_name.lower()
    if drug_name not in reviews:
        return "", "", "", "", "", "", "", ""

    positive_review_1 = reviews[drug_name]["positive"]["review1"]
    positive_rating_1 = reviews[drug_name]["positive"]["rating1"]
    positive_review_2 = reviews[drug_name]["positive"]["review2"]
    positive_rating_2 = reviews[drug_name]["positive"]["rating2"]

    negative_review_1 = reviews[drug_name]["negative"]["review1"]
    negative_rating_1 = reviews[drug_name]["negative"]["rating1"]
    negative_review_2 = reviews[drug_name]["negative"]["review2"]
    negative_rating_2 = reviews[drug_name]["negative"]["rating2"]

    return (
        positive_review_1,
        positive_rating_1,
        positive_review_2,
        positive_rating_2,
        negative_review_1,
        negative_rating_1,
        negative_review_2,
        negative_rating_2,
    )


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("query")
    medications = get_5_closest_drugs(query)
    return jsonify({"medications": medications})


@app.route("/update-query", methods=["POST"])
def update_query():
    query = request.json["query"]
    rel_docs = request.json["rel_docs"]
    non_rel_docs = request.json["non_rel_docs"]
    age = request.json["user_age"]
    medications_json = request.args.get("medications")
    if medications_json:
        medications = json.loads(medications_json)
    else:
        medications = []

    query += " " + " ".join(medications)

    new_query = rocchio(query, rel_docs, non_rel_docs)

    def combine_name(query, age):
        top_10 = query_after_rocchio(tfidf_matrix, query, age)
        rtrn_lst = []
        for tup in top_10:
            drug = tup[0]
            score = tup[1]
            component_1 = tup[2]
            component_score_1 = tup[3]
            component_2 = tup[4]
            component_score_2 = tup[5]
            component_3 = tup[6]
            component_score_3 = tup[7]
            reviews = get_reviews(drug)
            rtrn_lst.append(
                {
                    "drug": drug,
                    "definition": get_def(drug),
                    "score": score,
                    "top_5_ad_events": get_top_5_ad_events(drug),
                    "rating": get_rating(drug),
                    "median_age": get_median_age(drug),
                    "usage": get_usage(drug),
                    "component1": component_1,
                    "component_score1": component_score_1,
                    "component2": component_2,
                    "component_score2": component_score_2,
                    "component3": component_3,
                    "component_score3": component_score_3,
                    "positive_review_1": reviews[0],
                    "positive_rating_1": reviews[1],
                    "positive_review_2": reviews[2],
                    "positive_rating_2": reviews[3],
                    "negative_review_1": reviews[4],
                    "negative_rating_1": reviews[5],
                    "negative_review_2": reviews[6],
                    "negative_rating_2": reviews[7],
                }
            )
        return rtrn_lst

    return jsonify(combine_name(new_query, age))


@app.route("/drugs")
def drugs_search():
    text_query = request.args.get("query")
    age = float(request.args.get("age"))
    gender = request.args.get("gender")
    medications_json = request.args.get("medications")
    if medications_json:
        medications = json.loads(medications_json)
    else:
        medications = []

    text_query += " " + " ".join(medications)

    def combine_name(query, age):
        top_10 = query_with_age(tfidf_matrix, query, age)
        rtrn_lst = []
        for tup in top_10:
            drug = tup[0]
            score = tup[1]
            component_1 = tup[2]
            component_score_1 = tup[3]
            component_2 = tup[4]
            component_score_2 = tup[5]
            component_3 = tup[6]
            component_score_3 = tup[7]
            reviews = get_reviews(drug)
            rtrn_lst.append(
                {
                    "drug": drug,
                    "definition": get_def(drug),
                    "score": score,
                    "top_5_ad_events": get_top_5_ad_events(drug),
                    "rating": get_rating(drug),
                    "median_age": get_median_age(drug),
                    "usage": get_usage(drug),
                    "component1": component_1,
                    "component_score1": component_score_1,
                    "component2": component_2,
                    "component_score2": component_score_2,
                    "component3": component_3,
                    "component_score3": component_score_3,
                    "positive_review_1": reviews[0],
                    "positive_rating_1": reviews[1],
                    "positive_review_2": reviews[2],
                    "positive_rating_2": reviews[3],
                    "negative_review_1": reviews[4],
                    "negative_rating_1": reviews[5],
                    "negative_review_2": reviews[6],
                    "negative_rating_2": reviews[7],
                }
            )
        return rtrn_lst

    return jsonify(combine_name(text_query, age))


@app.route("/reviews")
def reviews():
    drug_name = request.args.get("drug_name")
    if not drug_name:
        return jsonify({"error": "No drug name provided"}), 400

    review_data = get_reviews(drug_name)

    return jsonify(review_data)


if "DB_NAME" not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5001)
