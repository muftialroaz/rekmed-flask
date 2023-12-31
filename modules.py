import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('indonesian'))  # Menggunakan kamus stop words Bahasa indonesia
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# nltk.download('punkt')
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from rank_bm25 import BM25Okapi

# Input preprocessing Function
def preprocess_input(input):
    ## Data cleaning
    # 1 Lowering case: Mengubah teks menjadi huruf kecil untuk konsistensi dalam analisis
    input = input.lower()

    # 2 Tokenisasi, memisahkan teks menjadi kata-kata atau frasa.
    input_tokens = word_tokenize(input)

    # 3 Menghapus Stopwords
    input_tokens = [word for word in input_tokens if word not in stop_words]

    # Membuat fungsi stemming untuk mengembalikan kata menjadi kata dasar
    def stem_text(text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stemmed_text = [stemmer.stem(word) for word in text]
        return stemmed_text

    # 4. Menjalankan fungsi stemming dari cell kode sebelumnnya
    input_tokens = stem_text(input_tokens)

    # 5. Menghapus kata yang terlalu pendek dan menyisakan minimal 3 huruf.
    min_length = 2  # Menentukan panjang minimum kata yang diizinkan

    input_tokens =  [word for word in input_tokens if len(word) >= min_length]

    # 6 Menggabungkan token menjadi teks bersih
    input_preprocess = [' '.join(input_tokens)]

    return input_preprocess

# Table text preprocessing
def preprocess(data_text):
    ## Data cleaning
    # 1 Lowering case: Mengubah teks menjadi huruf kecil untuk konsistensi dalam analisis
    data_text_nama = data_text.str.lower()

    data_text_nama = data_text_nama.apply(lambda x: re.sub('[^A-Za-z0-9.]+', ' ', x))

    # 2 Tokenisasi, memisahkan teks menjadi kata-kata atau frasa.
    data_text_nama_tokens = data_text_nama.apply(lambda x: word_tokenize(x))

    # 3 Menghapus Stopwords
    data_text_nama_tokens = data_text_nama_tokens.apply(lambda x: [word for word in x if word not in stop_words])

    # Membuat fungsi stemming untuk mengembalikan kata menjadi kata dasar
    def stem_text(text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stemmed_text = [stemmer.stem(word) for word in text]
        return stemmed_text

    # 4. Menjalankan fungsi stemming dari cell kode sebelumnnya
    data_text_nama_tokens = data_text_nama_tokens.apply(stem_text)

    # 5. Menghapus kata yang terlalu pendek dan menyisakan minimal 3 huruf.
    min_length = 2  # Menentukan panjang minimum kata yang diizinkan

    data_text_nama_tokens = data_text_nama_tokens.apply(lambda x: [word for word in x if len(word) >= min_length])

    # 6 Menggabungkan token menjadi teks bersih
    preprocess_text = data_text_nama_tokens.apply(lambda x: ' '.join(x))

    return preprocess_text

# Table text vectorization
def vektorisasi(data_text, input):
    # Inisialisasi CountVectorizer
    vectorizer = CountVectorizer()

    # Fit and transform on training data
    data_text_vec = vectorizer.fit_transform(data_text).toarray()
    input_vec = vectorizer.transform(input).toarray()

    # Convert to DataFrames for visualization (optional)
    df_text_vec = pd.DataFrame(data_text_vec, columns=vectorizer.get_feature_names_out())
    df_input_vec = pd.DataFrame(input_vec, columns=vectorizer.get_feature_names_out())

    return df_text_vec, df_input_vec


# Table text cosine similarity
def cosine_sim(data, input):
    cosine = []
    # Reshape the vectors to be 2D arrays
    for i in range(len(data)):
        vector1 = data.iloc[i:i+1]
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(vector1, input)
        cosine.append(cosine_sim[0][0])

    cosine_df = pd.DataFrame(cosine)
    cosine_df = cosine_df.rename(columns={0:'cosine'})
    # cosine_df = cosine_df.sort_values(by='cosine', ascending=False)

    return cosine_df

def bm_25(doc, input):
    # Pembentukan indeks BM25
    tokenized_documents = [doc.split() for doc in doc]
    bm25 = BM25Okapi(tokenized_documents)

    # Hitung relevansi BM25
    scores = bm25.get_scores(" ".join(input))

    ranked = pd.DataFrame(scores)
    ranked = ranked.rename(columns={0:'ranking'})

    return ranked