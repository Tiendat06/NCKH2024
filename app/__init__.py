import os
import pathlib
from flask import Flask, render_template, Blueprint, session
from flask_session import Session
from routes import routes
from dotenv import load_dotenv
from flask_cors import CORS
from google_auth_oauthlib.flow import Flow
from flask_sslify import SSLify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

# import streamlit as st
load_dotenv()

import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

# GOOGLE_CLIENT_ID = '439667677299-6ltpjf671e1cg2kmj3slqlqg2bnkmr91.apps.googleusercontent.com';
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json");

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
#     redirect_uri="http://127.0.0.1:5000/callback"
# );


cloudinary.config(
    cloud_name="dervs0fx5",
    api_key="195853691687668",
    api_secret="9b46KOOdA5y-Sc-C-KALItR1f3o",
    secure=True,
)

# change to https request (use for gmail)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# apps = Blueprint("app", __name__);

# @app.route('/', methods=['get'])
# def index():
#     return render_template('index.html')
# getApp(app)
# db = DataBaseUtils()



if __name__ == '__main__':
    app = Flask(__name__);
    ssl = SSLify(app);
    CORS(app)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JSON_AS_ASCII'] = False 
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER");
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_TLS");
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME");
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD");
    routes(app)
    app.run(debug=True)
