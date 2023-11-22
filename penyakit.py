import mysql.connector
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess, vektorisasi


db = mysql.connector.connect(
  host="localhost",
  user="muftialroaz",
  password="password",
  database="rekmed",
  port=3306
)

# Retrieve all records from the 'customers' table
cursor = db.cursor()
cursor.execute("SELECT rm_id, kode_root, nama FROM rm_diagnosis LEFT JOIN diagnosis ON diagnosis.kode = rm_diagnosis.kode;")

# Fetch all results as a list of tuples
diagnosis = cursor.fetchall()
diagnosis = pd.DataFrame(diagnosis)

diagnosis.columns = [str(x) for x in diagnosis.columns]
diagnosis.rename(columns={'0': 'mr', '2': 'nama'}, inplace=True)
diagnosis[['mr','nama']]

input = ['siti']
diagnosis = preprocess(diagnosis)
diagnosis_vec, input_vec = vektorisasi(diagnosis, input)
print(diagnosis_vec)
print(input_vec)