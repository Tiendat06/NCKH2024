import os
from flask import Flask, render_template, Blueprint
from routes import routes
from dotenv import load_dotenv
import streamlit as st
import subprocess
load_dotenv()

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
