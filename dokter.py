import mysql.connector
import pandas as pd
from modules import preprocess, vektorisasi, cosine_sim


db = mysql.connector.connect(
  host="localhost",
  user="muftialroaz",
  password="password",
  database="rekmed",
  port=3306
)

# Retrieve all records from the 'customers' table
cursor = db.cursor()
cursor.execute("SELECT user_id, nama, username FROM `dokter` LEFT JOIN `user` ON user.id = dokter.user_id;")

# Fetch all results as a list of tuples
dokter = cursor.fetchall()
dokter = pd.DataFrame(dokter)

dokter.columns = [str(x) for x in dokter.columns]
dokter.rename(columns={'0': 'mr', '2': 'nama'}, inplace=True)
dokter[['mr','nama']]

dokter_pre = preprocess(dokter['nama'])
def dokter_input(input):
  dokter_vec, input_vec = vektorisasi(dokter_pre, input)
  cosi = cosine_sim(dokter_vec, input_vec)
  return cosi