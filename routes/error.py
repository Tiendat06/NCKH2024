from flask import Blueprint
from app.controllers.ErrorController import ErrorController

error = Blueprint('error', __name__)

# [GET]
@error.app_errorhandler(Exception)
def index(error):
    return ErrorController().index(error)