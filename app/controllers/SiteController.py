from flask import render_template, session, redirect
from models.User import UserModel

class SiteController:
    def __init__(self):
        self.user = UserModel()
        
    # [GET]
    def home(self):
        if 'user' not in session:
            return redirect('/log/login')
        user = self.user.get_user()
        return render_template("home.html", user = user);