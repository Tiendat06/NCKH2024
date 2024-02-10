from flask import Blueprint
from controllers.AccountController import AccountController

account = Blueprint('account', __name__)

# [GET]
@account.route('/account', methods=['get'])
def index_none_pagination():
    return AccountController().index(1)

# [GET]
@account.route('/account/<pages>', methods=['get'])
def index(pages):
    return AccountController().index(pages)

# [GET]
@account.route('/account/changeRole/<role_name>/<acc_id>', methods=['get'])
def updateRole(role_name, acc_id):
    return AccountController().updateRole(role_name, acc_id)

# [GET]
@account.route('/account/resetPassword/<acc_id>', methods=['get'])
def resetPassword(acc_id):
    return AccountController().resetPassword(acc_id);
