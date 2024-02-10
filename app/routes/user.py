from flask import Blueprint
from controllers.UserController import UserController

user = Blueprint('user', __name__)

# [GET]
@user.route('/user', methods=['get'])
def index_none_pagination():
    return UserController().index(1)

# [GET]
@user.route('/user/<pages>', methods=['get'])
def index(pages):
    return UserController().index(pages)

# [POST]
@user.route('/user/add', methods=['post'])
def add_user():
    return UserController().add_user()

