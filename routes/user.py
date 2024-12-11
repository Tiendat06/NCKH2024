from flask import Blueprint
from app.controllers.UserController import UserController

user = Blueprint('user', __name__)

# [GET]
@user.route('/user', methods=['get'])
def index_none_pagination():
    return UserController().index(1)

# [GET]
@user.route('/user/<pages>', methods=['get'])
def index(pages):
    return UserController().index(pages)

# [POST, AJAX]
@user.route('/user/add', methods=['post'])
def add_user():
    return UserController().add_user()

# [POST, AJAX]
@user.route('/user/edit', methods=['post'])
def edit_user():
    return UserController().edit_user()

# [POST, AJAX]
@user.route('/user/delete', methods=['post'])
def delete_user():
    return UserController().delete_user()

@user.route('/user/profile', methods=['get'])
def user_profile():
    return UserController().user_profile();

@user.route('/user/profile/edit_personal_information', methods=['post'])
def edit_personal_information():
    return UserController().edit_personal_information();

@user.route('/user/get_user_info', methods=['get'])
def get_user_info():
    return UserController().get_user_info();

@user.route('/user/profile/change_pwd', methods=['post'])
def change_pwd():
    return UserController().change_pwd();