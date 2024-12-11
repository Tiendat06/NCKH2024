from flask import render_template, redirect
from app.models.Account import AccountModel
from app.models.User import UserModel

class AccountController:
    def __init__(self):
        self.account = AccountModel()
        self.user = UserModel()

    # [GET] /account
    def index(self, pages):
        user_db = self.user
        pages = int(pages);
        per_page = 10
        start = (pages - 1) * per_page
        end = start + per_page

        acc_data = self.user.get_account();
        acc_list, user_list = [], [];
        if acc_data:
            acc_list, user_list, role_list = acc_data;

        zip_data = zip(acc_list, user_list);
        zip_data_list = list(zip_data);
        total_pages = (len(zip_data_list) + per_page - 1) // per_page;
        items_on_page = zip_data_list[start: end];
        # print(start)
        # print(end)

        return redirect("/") if self.account.checkRole() else render_template("index.html", content='index', page='account', zip_data=items_on_page, total_pages=total_pages, pages=pages);

    # [GET] /account/changeRole/<role_name>/<acc_id>
    def updateRole(self, role_name, acc_id):
        # self.account.checkRole();
        self.account.updateRole(role_name, acc_id);
        return redirect("/") if self.account.checkRole() else redirect("/account");
    
    # [GET] /account/resetPassword/<acc_id>
    def resetPassword(self, acc_id):
        # self.account.checkRole();
        self.user.resetPassword(acc_id);
        return redirect("/") if self.account.checkRole() else redirect("/account");
    
    
    




        
