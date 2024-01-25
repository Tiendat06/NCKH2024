from flask import Blueprint
from controllers.AccountController import AccountController

account = Blueprint('account', __name__)
@account.route('/account', methods=['get'])
def index():
    return AccountController().index()

