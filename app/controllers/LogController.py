from flask import render_template, request, session, redirect, make_response, jsonify
from datetime import datetime
from models.Account import Account, AccountModel
from models.User import User, UserModel
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer
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

        error = '';
        print(self.account.checkLogin(data)[1])
        
        if self.account.checkLogin(data)[0]:
            session['account'] = email;
            user = self.user.get_user_by_email(email);
            response = make_response(redirect('/'));
            # Thiết lập cookie trên đối tượng response
            response.set_cookie('user_name', user._name)
            response.set_cookie('user_img', user._img_profile)
            session['user_name'] = user._name;
            session['user_img'] = user._img_profile;
            session['user_id'] = user._user_id;
            session['acc_id'] = user._acc_id;
            # print(user._name);
            # print(user._img_profile);
            
            return response
        elif not self.account.checkLogin(data)[0] and self.account.checkLogin(data)[1] == 'ROL0000003':
            error = 'Your account has been banned!';
            return render_template("/log/login.html", error=error);
        else:
            error = "Invalid email or password !";
            return render_template("/log/login.html", error=error)
        
    # [GET]
    def logout(self):
        session.clear();
        return redirect('/')
    
    # [GET]
    def register(self):
        return render_template('/log/login.html', register="register")
    
    # [POST]
    def registerPost(self):
        user_db = self.user;
        fullname = request.form.get('fullname');
        phone = request.form.get('phone')
        email = request.form.get('email')

        if user_db.checkEmailIsContain(email): 
            return render_template('/log/login.html', register="register", result = 'Your email has been contained !')
        pwd = request.form.get('pwd')
        # date = request.form.get('date')
        date_to_db = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()

        # get datetime no need format
        # date_to_db = datetime(date.year, date.month, date.day)

        # format to string because only datetime is allowed
        date_formatted = date_to_db.strftime('%Y-%m-%d')
        gender = request.form.get('gender')

        default_img_profile = 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png'

        user = User('', '', '', fullname, gender, email, date_formatted, phone, default_img_profile)
        account = Account('', '', pwd, '', 'ROL0000002');
        # print(user)
        # print(account)

        result = self.user.createAccount(user, account);
        return render_template('/log/login.html', register="register", result = result)



        
