from flask import Blueprint
from controllers.LogController import LogController

log = Blueprint('log', __name__)
# login
# [GET]
@log.route('/log/login', methods=['get'])
def login():
    return LogController().login()

# [POST]
@log.route('/log/login', methods=['post'])
def loginPost():
    return LogController().loginPost()

# logout
# [GET]
@log.route('/log/logout', methods=['get'])
def logout():
    return LogController().logout()

# register
# [GET]
@log.route('/log/register', methods=['get'])
def register():
    return LogController().register()

# [POST]
@log.route('/log/register', methods=['post'])
def registerPost():
    return LogController().registerPost()

# log.add_url_rule('/log/login', 'loginPost', LogController.loginPost(), methods=['POST'])
