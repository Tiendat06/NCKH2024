from flask import Blueprint
from controllers.AccountController import AccountController

account = Blueprint('account', __name__)

@account.route('/account', methods=['get'])
def index_none_pagination():
    return AccountController().index(1)

@account.route('/account/<pages>', methods=['get'])
def index(pages):
    return AccountController().index(pages)

@account.route('/account/changeRole/<role_name>/<acc_id>', methods=['get'])
def updateRole(role_name, acc_id):
    return AccountController().updateRole(role_name, acc_id)

@account.route('/account/resetPassword/<acc_id>', methods=['get'])
def resetPassword(acc_id):
    return AccountController().resetPassword(acc_id);
