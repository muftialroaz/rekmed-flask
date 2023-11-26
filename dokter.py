import pandas as pd
from modules import preprocess, vektorisasi, cosine_sim, bm_25
import db

rekam_medis_df = db.rekam_medis
dokter_pre = preprocess(rekam_medis_df['dokter_nama'])

def dokter_data(input):
  pasien_vec, input_vec = vektorisasi(dokter_pre, input)
  cosi = cosine_sim(pasien_vec, input_vec)

  # gabungkan dalam satu dataframe
  df_vector = pd.concat([rekam_medis_df, cosi], axis=1) 
  # df_vector = df_vector.sort_values(by='cosine', ascending=False)

  # selected_names = df_vector.loc[df_vector['cosine'] > 0, 'dokter_nama']
  # selected_names = df_vector[df_vector['cosine'] > 0]

  return df_vector

def dokter_bm25(input):
  df_vector = bm_25(dokter_pre, input)
  # gabungkan dalam satu dataframe
  df_vector = pd.concat([rekam_medis_df, df_vector['ranking']], axis=1) 

  return df_vector