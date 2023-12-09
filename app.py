from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect
from modules import preprocess_input, preprocess, vektorisasi, cosine_sim
import pandas as pd
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
        keyword = preprocess_input(input_data)

        rekam_medis = db.rekam_medis.copy()
        rekam_medis['combined_text'] = rekam_medis['pasien_nama'] + ' ' + rekam_medis['diagnosis_nama'] + ' ' + rekam_medis['dokter_nama']
        
        doc_pre = preprocess(rekam_medis['combined_text'])
        doc_vec, keyword_vec = vektorisasi(doc_pre, keyword)
        cosi = cosine_sim(doc_vec, keyword_vec)

        # gabungkan dalam satu dataframe
        rekam_medis = pd.concat([rekam_medis, cosi], axis=1) 
        rekam_medis.sort_values(by='cosine', ascending=False)

        rekam_medis = rekam_medis[rekam_medis['cosine'] > 0]

        json = rekam_medis.to_dict(orient='index')

        return jsonify(json)

    if request.method == 'POST':
        search_keyword_from_yii_post = request.get_json().get('q', '')
        search_keyword_from_post = search_keyword_from_yii_post
        print(f"Search keyword from Yii (POST): {search_keyword_from_yii_post}")

        input_data = search_keyword_from_yii_post
        keyword = preprocess_input(input_data)

        rekam_medis = db.rekam_medis.copy()
        rekam_medis['combined_text'] = rekam_medis['pasien_nama'] + ' ' + rekam_medis['diagnosis_nama'] + ' ' + rekam_medis['dokter_nama']
        
        doc_pre = preprocess(rekam_medis['combined_text'])
        doc_vec, keyword_vec = vektorisasi(doc_pre, keyword)
        cosi = cosine_sim(doc_vec, keyword_vec)

        # gabungkan dalam satu dataframe
        rekam_medis = pd.concat([rekam_medis, cosi], axis=1) 
        rekam_medis.sort_values(by='cosine', ascending=False)

        rekam_medis = rekam_medis[rekam_medis['cosine'] > 0]

        json = rekam_medis.to_dict(orient='index')

        return jsonify(json)

if __name__ == '__main__':
    app.run(debug=True)
