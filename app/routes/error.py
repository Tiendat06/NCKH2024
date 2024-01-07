from flask import Blueprint
from controllers.ErrorController import ErrorController

error = Blueprint('error', __name__)

@error.app_errorhandler(Exception)
def index(error):
    return ErrorController().index(error)