from flask import Blueprint
from controllers.LogController import LogController

log = Blueprint('log', __name__)
# login
@log.route('/log/login', methods=['get'])
def login():
    return LogController().login()

@log.route('/log/login', methods=['post'])
def loginPost():
    return LogController().loginPost()

# logout
@log.route('/log/logout', methods=['get'])
def logout():
    return LogController().logout()

# register
@log.route('/log/register', methods=['get'])
def register():
    return LogController().register()

# log.add_url_rule('/log/login', 'loginPost', LogController.loginPost(), methods=['POST'])
