from flask import Flask, request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect
from pasien import pasien_data
from diagnosis import diagnosis_data
from dokter import dokter_data
from modules import preprocess_input
import db

app = Flask(__name__)
csrf = CSRFProtect(app)

# Variable to store the search keyword from Yii
search_keyword_from_post = ''

# Define a handler for POST requests at the '/' route
@app.route('/', methods=['GET', 'POST'])
@csrf.exempt
def index():
    global search_keyword_from_post

    print(f"Received {request.method} request to {request.path}")

    if request.method == 'GET':
        search_keyword_from_yii_get = search_keyword_from_post
        print(f"Search keyword from Yii (GET): {search_keyword_from_yii_get}")

        input_data = search_keyword_from_yii_get
        preprocessed_input = preprocess_input(input_data)

        nama_pasien = pasien_data(preprocessed_input)
        diagnosis = diagnosis_data(preprocessed_input)
        nama_dokter = dokter_data(preprocessed_input)

        rekam_medis = db.rekam_medis.copy()
        rekam_medis['cosine'] = (nama_pasien['cosine'] + diagnosis['cosine'] + nama_dokter['cosine']) / 3
        rekam_medis = rekam_medis.sort_values(by='cosine', ascending=False)
        rekam_medis = rekam_medis[rekam_medis['cosine'] > 0]

        json = rekam_medis.to_dict(orient='index')

        # diagnosis_nama = rekam_medis['diagnosis_nama'].tolist()
        # pasien_nama = rekam_medis['pasien_nama'].tolist()
        # dokter_nama = rekam_medis['dokter_nama'].tolist()
        # cosine = rekam_medis['cosine'].tolist()

        # return render_template('index.jinja', input_data=input_data, nama_pasien=pasien_nama, diagnosis=diagnosis_nama, nama_dokter=dokter_nama, cosine=cosine)
        return jsonify(json)

    if request.method == 'POST':
        search_keyword_from_yii_post = request.get_json().get('q', '')
        search_keyword_from_post = search_keyword_from_yii_post
        print(f"Search keyword from Yii (POST): {search_keyword_from_yii_post}")

        input_data = search_keyword_from_yii_post
        preprocessed_input = preprocess_input(input_data)

        nama_pasien = pasien_data(preprocessed_input)
        diagnosis = diagnosis_data(preprocessed_input)
        nama_dokter = dokter_data(preprocessed_input)

        rekam_medis = db.rekam_medis.copy()
        rekam_medis['cosine'] = (nama_pasien['cosine'] + diagnosis['cosine'] + nama_dokter['cosine']) / 3
        rekam_medis = rekam_medis[rekam_medis['cosine'] > 0]
        rekam_medis = rekam_medis.sort_values(by='cosine', ascending=False)

        json = rekam_medis.to_dict(orient='index')

        diagnosis_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'diagnosis_nama'].tolist()
        pasien_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'pasien_nama'].tolist()
        dokter_nama = rekam_medis.loc[rekam_medis['cosine'] > 0, 'dokter_nama'].tolist()
        cosine = rekam_medis.loc[rekam_medis['cosine'] > 0, 'cosine'].tolist()

        return jsonify(json)

if __name__ == '__main__':
    app.run(debug=True)
