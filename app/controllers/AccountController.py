from flask import render_template, request, session, redirect
from models.Account import Account, AccountModel
from config import DataBaseUtils
class AccountController:
    def __init__(self):
        self.account = AccountModel()

    # [GET]
    def index(self):
        acc_list = self.account.get_account();
        return render_template("index.html", content='index', page='account', acc_list = acc_list);



        
