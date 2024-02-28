from flask import request, render_template, redirect, jsonify
from models.User import UserModel, User
from models.Account import Account, AccountModel

class UserController:
    def __init__(self):
        self.user = UserModel()
        self.account = AccountModel()

    # [GET]
    def index(self, pages):
        user_db = self.user;
        pages = int(pages);
        per_page = 8;
        start = (pages - 1) * per_page;
        end = start + per_page

        user_data = user_db.get_account();
        user_list = []
        if user_data:
            acc_list, user_list, role_list = user_data;
        
        zip_data = zip(acc_list, user_list, role_list)
        zip_data_list = list(zip_data)
        total_pages = (len(zip_data_list) + per_page - 1) // per_page
        items_on_page = zip_data_list[start: end]

        print(start)
        print(end)

        return render_template("index.html", content='index', page='user', zip_data=items_on_page, total_pages=total_pages, pages=pages)
    
    # [POST, AJAX]
    def add_user(self):
        user_db = self.user;
        acc_db = self.account;
        result = {
            'empty': 'Please fill out all fields !',
            'error': 'Your email has been contained !',
            'success': 'Add Successfully !',
        }

        user_id = user_db.AUTO_USE_ID();
        acc_id = acc_db.AUTO_ACC_ID();
        data = request.get_json();

        name = data.get('name');
        gender = data.get('gender');
        email = data.get('email');
        dob = data.get('dob');
        phone = data.get('phone');

        print(name)
        print(gender)
        print(email)
        print(dob)
        print(phone)
        
        if not all([name, gender, email, dob, phone]):
            return jsonify(result.get('empty'))

        # name = request.form.get('full_name_add');
        # gender = request.form.get('gender_add');
        # email = request.form.get('email_add');
        # dob = request.form.get('dob_add');
        # phone = request.form.get('phone_add');
        img_profile = 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png'


        if user_db.checkEmailIsContain(email):
            return jsonify(result.get('error'))

        user = User('', user_id, acc_id, name, gender, email, dob, phone, img_profile);
        account = Account('', '', email, acc_id, 'ROL0000002');

        user_db.createAccount(user, account);
        return jsonify(result.get('success'));
    
            
