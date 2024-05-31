from flask import abort, render_template, request, session, redirect, make_response, jsonify, url_for
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

import requests
from models.Account import Account, AccountModel
from models.User import User, UserModel
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask_mail import Message, Mail

class LogController:
    def __init__(self):
        self.account = AccountModel()
        self.user = UserModel();
    
    # [GET] /log/login_gmail
    def loginByGoogle(self, flow):
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    # [GET] /log/login
    def login(self):
        if 'account' in session:
            return redirect('/')
        return render_template('/log/login.html');

    # [GET] /log/callback
    def callback(self, flow, GOOGLE_CLIENT_ID):
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10,
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        email = session["account"] = id_info.get("email");
        user = self.user.get_user_by_email(email);
        session['user_name'] = user._name;
        session['user_img'] = user._img_profile;
        session['user_id'] = user._user_id;
        session['acc_id'] = user._acc_id;
        account = self.account.findAccountByAccId(user._acc_id);
        if account._role_id == 'ROL0000003':
            error = 'Your account has been banned!';
            return render_template("/log/login.html", error=error);
        return redirect("/");

    def protected_area(self):
        print(session.get("account"))
        return "Hi world";

    # [POST] /log/login
    def loginPost(self):
        email = request.form.get("email");
        pwd = request.form.get("pwd");
        data = {
            'email': email,
            'password': pwd
        }
        # print(data)

        error = '';
        # print(self.account.checkLogin(data)[1])
        
        if self.account.checkLogin(data)[0]:
            session['account'] = email;
            user = self.user.get_user_by_email(email);
            session['google_id'] = "Test";

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
        elif (not self.account.checkLogin(data)[0]) or self.account.checkLogin(data)[1] == 'ROL0000003':
            error = 'Your account has been banned!';
            return render_template("/log/login.html", error=error);
        else:
            error = "Invalid email or password !";
            return render_template("/log/login.html", error=error)
        
    # [GET] /log/login
    def logout(self):
        google_id = session.get("google_id");
        session.clear();
        session['google_id'] = google_id;
        return redirect('/')
    
    # [GET] /log/register
    def register(self):
        return render_template('/log/login.html', register="register")
    
    # [POST] /log/register
    def registerPost(self, app):
        mail = Mail(app);
        
        user_db = self.user;
        acc_db = self.account;

        user_id = user_db.AUTO_USE_ID();
        acc_id = acc_db.AUTO_ACC_ID();

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

        user = User('', user_id, '', fullname, gender, email, date_formatted, phone, default_img_profile)
        account = Account('', '', pwd, acc_id, 'ROL0000003');

        result = self.user.createAccount(user, account);
        session['acc_id'] = acc_id;

        s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"));
        token = s.dumps(email, salt='email-confirms');
        msg = Message('Confirm Email', sender='tiendat79197@gmail.com', recipients=[email]);
        confirm_url = url_for('log.confirm_email', token=token, _external=True);
        # OTPcode = user_db.generateOTPcode();

        msg.body = f'Get link below to confirm your email, you only have 5 minutes to do thist action:\n{confirm_url}\n';
        mail.send(msg);
        return render_template('/log/login.html', register="register", result = result)

    def confirm_email(self, token):
        # print("sec key:",os.getenv("SECRET_KEY"));
        if 'account' in session:
            s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"));
            acc_db = self.account;
            try:
                email = s.loads(token, salt='email-confirms', max_age=300);
                acc_id = session.get('acc_id');
                account = self.account.findAccountByAccId(acc_id);
                if account:
                    session.pop('acc_id');
                    role_id = 'ROL0000002';
                    acc_db.updateRoleById(acc_id, role_id);
                else:
                    return redirect("/");
                return render_template("/log/verified.html");
            except SignatureExpired:
                return render_template("/log/failed.html");
        return redirect("/");



        
