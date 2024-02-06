from flask import Blueprint
from controllers.UserController import UserController

user = Blueprint('user', __name__)

@user.route('/user', methods=['get'])
def index_none_pagination():
    return UserController().index(1)

@user.route('/user/<pages>', methods=['get'])
def index(pages):
    return UserController().index(pages)

@user.route('/user/add', methods=['post'])
def add_user():
    return UserController().add_user()

