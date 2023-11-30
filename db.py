import mysql.connector
import pandas as pd

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="rekmed",
  port=3306
)

# Retrieve all records from the 'customers' table
cursor = db.cursor()
# cursor.execute("SELECT rekam_medis.rm_id, rm_diagnosis.nama_diagnosis, dokter.user_id AS dokter_user_id, dokter.nama AS dokter_nama, user.username AS dokter_username, pasien.mr AS pasien_mr, pasien.nama AS pasien_nama FROM rekam_medis LEFT JOIN dokter ON rekam_medis.user_id = dokter.user_id LEFT JOIN rm_diagnosis ON rekam_medis.rm_id = rm_diagnosis.rm_id LEFT JOIN pasien ON rekam_medis.mr = pasien.mr LEFT JOIN user ON dokter.user_id = user.id;")
cursor.execute("SELECT rekam_medis.rm_id, rm_diagnosis.nama_diagnosis, dokter.user_id AS dokter_user_id, dokter.nama AS dokter_nama, user.username AS dokter_username, pasien.mr AS pasien_mr, pasien.nama AS pasien_nama, kunjungan.tanggal_periksa FROM rekam_medis LEFT JOIN dokter ON rekam_medis.user_id = dokter.user_id LEFT JOIN rm_diagnosis ON rekam_medis.rm_id = rm_diagnosis.rm_id LEFT JOIN pasien ON rekam_medis.mr = pasien.mr LEFT JOIN user ON dokter.user_id = user.id LEFT JOIN kunjungan on rekam_medis.kunjungan_id = kunjungan.kunjungan_id;")

# Fetch all results as a list of tuples
rekam_medis = cursor.fetchall()
rekam_medis = pd.DataFrame(rekam_medis)
# rekam_medis.rename(columns={0: 'rm_id', 1: 'diagnosis_nama', 2:"dokter_user_id", 3: 'dokter_nama', 4: "dokter_username", 5: "pasien_mr", 6:"pasien_nama"}, inplace=True)
rekam_medis.rename(columns={0: 'rm_id', 1: 'diagnosis_nama', 2:"dokter_user_id", 3: 'dokter_nama', 4: "dokter_username", 5: "pasien_mr", 6:"pasien_nama", 7:"tanggal_periksa"}, inplace=True)
rekam_medis = rekam_medis.fillna('Kosong')

cursor.close()
db.close()