from flask import request, render_template, redirect
from models.User import UserModel

class UserController:
    def __init__(self):
        self.user = UserModel()

    def index(self, pages):
        user_db = self.user;
        pages = int(pages);
        per_page = 10;
        start = (pages - 1) * per_page;
        end = start + per_page

        user_data = user_db.get_account();
        user_list = []
        if user_data:
            user_list = user_data[1];
        total_pages = (len(user_list) + per_page - 1) // per_page
        items_on_page = user_list[start: end]

        return render_template("index.html", content='index', page='user', user_list=items_on_page, total_pages=total_pages, pages=pages)
    
    def add_user(self):
        return redirect('/user')