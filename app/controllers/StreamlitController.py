from flask import render_template, session, redirect
from models.Account import AccountModel
import streamlit as st
# import yfinance as yf
import subprocess

class StreamlitController:
    def __init__(self):
        pass

    def index(self):
        # Gọi streamlit như một quy trình con
        # , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        subprocess.call(['streamlit', 'run', 'streamlit_app.py'])

        return "Streamlit is running at http://localhost:8501"