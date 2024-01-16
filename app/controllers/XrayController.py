from flask import render_template, session, redirect
from models.Account import AccountModel
from config import DataBaseUtils

class XrayController:
    def __init__(self):
        self.account = AccountModel();

    def index(self):

        return render_template("index.html", content = 'index', page = 'xray')