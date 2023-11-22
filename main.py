# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

from pasien import pasien_input
from penyakit import penyakit_input
from dokter import dokter_input
from modules import preprocess

input = [input()]
# input = preprocess(input)

print(pasien_input(input))
print(penyakit_input(input))
print(dokter_input(input))