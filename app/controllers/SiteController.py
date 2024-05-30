from flask import render_template, session, redirect
from models.Account import AccountModel

class SiteController:
    def __init__(self):
        self.account = AccountModel()

    # [GET] /
    def index(self):
        if 'account' not in session:
            return redirect('/home')
        
        return render_template("index.html", content = 'index', page = 'index')
        
    # [GET] /home
    def home(self):
        if 'account' in session:
            return redirect('/')
        return render_template("index.html", content = 'home');