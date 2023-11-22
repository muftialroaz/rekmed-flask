# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

from pasien import pasien_input
from penyakit import penyakit_input
from dokter import dokter_input
from modules import preprocess_input

input = input()
input = preprocess_input(input)
print(input)

print('NAMA PASIEN', pasien_input(input))
print('DIAGNOSIS', penyakit_input(input))
print('NAMA DOKTER' ,dokter_input(input))