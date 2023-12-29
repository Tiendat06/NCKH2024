from flask import render_template, request, session, redirect
from models.User import User, UserModel
from config import DataBaseUtils
class LogController:
    def __init__(self):
        self.user = UserModel()

    # [GET]
    def login(self):
        if 'user' in session:
            return redirect('/')
        return render_template('login.html');

    # [POST]
    def loginPost(self):
        # conn = DataBaseUtils.get_connection()
        # user = UserModel()
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        data = {
            'email': email,
            'password': pwd
        }
        
        if self.user.checkLogin(data):
            session['user'] = email
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid email or password !")
        
    # [GET]
    def logout(self):
        session.clear();
        return redirect('/')
    
    # [GET]
    def register(self):
        return render_template('login.html', register="register")


        
