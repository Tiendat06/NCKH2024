import os
from flask import Flask, render_template, Blueprint
from routes import routes
from dotenv import load_dotenv
# import streamlit as st
load_dotenv()

import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

from my_yolov6 import my_yolov6


cloudinary.config(
    cloud_name="dervs0fx5",
    api_key="195853691687668",
    api_secret="9b46KOOdA5y-Sc-C-KALItR1f3o",
    secure=True,
)


# apps = Blueprint("app", __name__);

# @app.route('/', methods=['get'])
# def index():
#     return render_template('index.html')
# getApp(app)
# db = DataBaseUtils()

if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    routes(app)
    app.run(debug=True)
    # st.rerun()
