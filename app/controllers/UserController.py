from flask import request, render_template, redirect, jsonify
from models.User import UserModel, User
from models.Account import Account, AccountModel
import cloudinary.uploader

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
        img_profile = 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png'
        
        if not all([name, gender, email, dob, phone]):
            return jsonify(result.get('empty'))

        if user_db.checkEmailIsContain(email):
            return jsonify(result.get('error'))

        user = User('', user_id, acc_id, name, gender, email, dob, phone, img_profile);
        account = Account('', '', email, acc_id, 'ROL0000002');

        user_db.createAccount(user, account);
        return jsonify(result.get('success'));
    
    # POST, AJAX
    def edit_user(self):
        user_db = self.user;
        result = {
            'fail': 'Edit failed !',
            'error': 'Your email has been contained !',
            'empty': 'You must to fill out all fields except avatar !',
            'success': 'Edit successfully !'
        }

        data = request.get_json();
        name = data.get('name');
        gender = data.get('gender');
        email = data.get('email');
        tmp_email = data.get('tmp_email');
        dob = data.get('dob');
        phone = data.get('phone');
        # img_profile = request.files['file']
        user_id = data.get('user_id');
        acc_id = data.get('acc_id');
        img = data.get('img');
        # name = request.form['name']
        # gender = request.form['gender']
        # email = request.form['email']
        # dob = request.form['dob']
        # phone = request.form['phone']
        # tmp_email = request.form['tmp_email']
        # user_id = request.form['user_id']
        # acc_id = request.form['acc_id']
        
        # img_profile = request.files['avatar']  # Lấy file từ yêu cầu

        # print(name)
        # print(gender)
        # print(email)
        # print(dob)
        # print(phone)
        # print(img_profile)
        # avatar = None;
        # still bugs
        # if img_profile is None or img_profile == "":
            # avatar = 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png'
        # else:
        #     res = cloudinary.uploader.upload(img_profile);
        #     avatar = res['secure_url'];
        # 
        # print(img_profile)
        # print(user_id)
        # print(acc_id)
        # print(avatar);
        

        if not all([name, gender, email, dob, phone]):
            return jsonify(result.get('empty'))

        if user_db.checkEmailIsContain(email) and email != tmp_email:
            return jsonify(result.get('error'))
        
        user = User('', user_id, acc_id, name, gender, email, dob, phone, img);
        if not user:
            return jsonify(result.get('fail'));
        edit = user_db.edit_user(user)
        if not edit:
            return jsonify(result.get('fail'));

        return jsonify(result.get('success'));
