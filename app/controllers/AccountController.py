from flask import render_template, request, session, redirect
from models.Account import Account, AccountModel
from config import DataBaseUtils
class AccountController:
    def __init__(self):
        self.account = AccountModel()

    # [GET]
    def index(self):
        return render_template("index.html", content='index', page='account');



        
