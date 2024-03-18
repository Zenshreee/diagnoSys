import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="definitions_db"
)

cursor = conn.cursor()

query = 'SELECT * FROM definitions'

cursor.execute(query)

# for row in cursor.fetchall():

conn.close()



def json_to_tfidf(path: str) -> csr_matrix:
    with open(path, "r") as file:
        adverse_to_webster = json.load(file)
    