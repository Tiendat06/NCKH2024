from flask import render_template, request, session, redirect
from datetime import datetime
from models.Account import Account, AccountModel
from models.User import User, UserModel
from config import DataBaseUtils
class LogController:
    def __init__(self):
        self.account = AccountModel()
        self.user = UserModel();

    # [GET]
    def login(self):
        if 'account' in session:
            return redirect('/')
        return render_template('/log/login.html');

    # [POST]
    def loginPost(self):
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        data = {
            'email': email,
            'password': pwd
        }
        
        if self.account.checkLogin(data):
            session['account'] = email
            return redirect('/')
        else:
            return render_template("/log/login.html", error="Invalid email or password !")
        
    # [GET]
    def logout(self):
        session.clear();
        return redirect('/')
    
    # [GET]
    def register(self):
        return render_template('/log/login.html', register="register")
    
    # [POST]
    def registerPost(self):
        fullname = request.form.get('fullname');
        phone = request.form.get('phone')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        # date = request.form.get('date')
        date_to_db = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()

        # get datetime no need format
        # date_to_db = datetime(date.year, date.month, date.day)

        # format to string because only datetime is allowed
        date_formatted = date_to_db.strftime('%Y-%m-%d')
        gender = request.form.get('gender')

        user = User('', '', '', fullname, gender, email, date_formatted, phone)
        account = Account('', '', pwd, '', 'ROL0000002');
        # print(user)
        # print(account)

        result = self.user.add_user(user, account);
        return render_template('/log/login.html', register="register", result = result)



        
