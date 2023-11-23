import pandas as pd
from modules import preprocess, vektorisasi, cosine_sim
import db

rekam_medis_df = db.rekam_medis
diagnosis_pre = preprocess(rekam_medis_df['diagnosis_nama'])

def diagnosis_data(input):
  pasien_vec, input_vec = vektorisasi(diagnosis_pre, input)
  cosi = cosine_sim(pasien_vec, input_vec)

  # gabungkan dalam satu dataframe
  df_vector = pd.concat([rekam_medis_df, cosi], axis=1) 
  # df_vector = df_vector.sort_values(by='cosine', ascending=False)

  selected_names = df_vector.loc[df_vector['cosine'] > 0, 'diagnosis_nama']

  return selected_names