from flask import Blueprint, abort, session, redirect
from controllers.SiteController import SiteController

site = Blueprint('site', __name__)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            # return abort(401)  # Authorization required
            return redirect("/home");
        else:
            return function()

    return wrapper

# [GET]
@site.route('/home', methods=['get'])
def index():
    return SiteController().home();

# [GET]
@site.route('/', methods=['get'])
@login_is_required
def home():
    return SiteController().index();