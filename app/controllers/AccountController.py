from flask import render_template, request, session, redirect
from models.Account import Account, AccountModel
from models.User import User, UserModel

class AccountController:
    def __init__(self):
        self.account = AccountModel()
        self.user = UserModel()

    # [GET]
    def index(self, pages):
        user_db = self.user

        pages = int(pages);
        per_page = 10
        start = (pages - 1) * per_page
        end = start + per_page

        acc_data = self.user.get_account()
        acc_list, user_list = [], []
        if acc_data:
            acc_list, user_list, role_list = acc_data

        zip_data = zip(acc_list, user_list)
        zip_data_list = list(zip_data)
        total_pages = (len(zip_data_list) + per_page - 1) // per_page
        items_on_page = zip_data_list[start: end]
        # print(start)
        # print(end)

        return render_template("index.html", content='index', page='account', zip_data=items_on_page, total_pages=total_pages, pages=pages)

    # [GET]
    def updateRole(self, role_name, acc_id):
        self.account.updateRole(role_name, acc_id)
        return redirect("/account")
    
    # [GET]
    def resetPassword(self, acc_id):
        self.user.resetPassword(acc_id)
        return redirect("/account")
    




        
