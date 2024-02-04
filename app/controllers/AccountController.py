from flask import render_template, request, session, redirect
from models.Account import Account, AccountModel
from models.User import User, UserModel
from config import DataBaseUtils
class AccountController:
    def __init__(self):
        self.account = AccountModel()
        self.user = UserModel()

    # [GET]
    def index(self):
        page = request.args.get('page', 1, type=int)
        per_page = 10;
        skip = (page - 1) * per_page;
        acc_list = self.user.get_account()[0];
        user_list = self.user.get_account()[1];
        zip_data = zip(acc_list, user_list)

        # for acc, user in zip_data:
        #     print(f"Account Pass: {acc._password}")
        #     print(f"Username: {user._name}")
        return render_template("index.html", content='index', page='account', zip_data = zip_data);

    def updateRole(self, role_name, acc_id):
        self.account.updateRole(role_name, acc_id)
        return redirect("/account")
    
    def resetPassword(self, acc_id):
        self.user.resetPassword(acc_id)
        return redirect("/account")




        
