from flask import Flask, render_template, request
from pasien import pasien_data
from diagnosis import diagnosis_data
from dokter import dokter_data
from modules import preprocess_input
import db

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_data = request.form.get("input_data")
        preprocessed_input = preprocess_input(input_data)

        nama_pasien = pasien_data(preprocessed_input)
        diagnosis = diagnosis_data(preprocessed_input)
        nama_dokter = dokter_data(preprocessed_input)

        rekam_medis = db.rekam_medis.copy()
        # rekam_medis['cosine'] = (nama_pasien['cosine'] + diagnosis['cosine'] + nama_dokter['cosine']) / 3
        rekam_medis['cosine'] = nama_dokter['cosine']
        rekam_medis = rekam_medis.sort_values(by='cosine', ascending=False)

        diagnosis_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'diagnosis_nama'].tolist()
        pasien_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'pasien_nama'].tolist()
        dokter_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'dokter_nama'].tolist()
        cosine = rekam_medis.loc[rekam_medis['cosine'] > 0, 'cosine'].tolist()

        # return render_template('index.html', input_data=input_data, nama_pasien=nama_pasien, diagnosis=diagnosis, nama_dokter=nama_dokter)
        return render_template('index.jinja', input_data=input_data, nama_pasien=pasien_nama, diagnosis=diagnosis_nama, nama_dokter=dokter_nama, cosine=cosine)

    return render_template('form.jinja')  # Render form jika metodenya adalah GET

if __name__ == "__main__":
    app.run()  # Gunakan manager untuk menjalankan aplikasi