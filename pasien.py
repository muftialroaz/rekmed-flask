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
cursor.execute("SELECT * FROM pasien")

# Fetch all results as a list of tuples
pasien = cursor.fetchall()
pasien = pd.DataFrame(pasien)

pasien.columns = [str(x) for x in pasien.columns]
pasien.rename(columns={'0': 'mr', '2': 'nama'}, inplace=True)
pasien[['mr','nama']]

input = ['siti']
pasien = preprocess(pasien)
pasien_vec, input_vec = vektorisasi(pasien, input)
print(pasien_vec)
print(input_vec)