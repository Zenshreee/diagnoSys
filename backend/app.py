import json
import os
from preprocessing.tfidf import tfidf_matrix, query_with_age
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ["ROOT_PATH"] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = "hfes2003"
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
    return top_5[drug_name][:5]


def get_rating(drug_name):
    pathdir = os.path.dirname(__file__)
    datadir = os.path.join(pathdir, "preprocessing", "average_ratings.json")
    with open(datadir, "r") as file:
        ratings = json.load(file)
    if drug_name not in ratings:
        return -1
    return ratings[drug_name]


@app.route("/drugs")
def drugs_search():
    text_query = request.args.get("query")
    age = float(request.args.get("age"))

    def combine_name(query, age):
        top_10 = query_with_age(tfidf_matrix, query, age)
        rtrn_lst = []
        for tup in top_10:
            rtrn_lst.append(
                {
                    "drug": tup[0],
                    "definition": get_def(tup[0]),
                    "score": tup[1],
                    "top_5_ad_events": get_top_5_ad_events(tup[0]),
                    "rating": get_rating(tup[0]),
                }
            )
        return rtrn_lst

    return jsonify(combine_name(text_query, age))


if "DB_NAME" not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
