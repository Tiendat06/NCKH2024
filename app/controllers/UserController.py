from flask import request, render_template, redirect
from models.User import UserModel

class UserController:
    def __init__(self):
        self.user = UserModel()

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
    
    # [POST]
    def add_user(self):
        return redirect('/user')