from flask import Blueprint
from controllers.SiteController import SiteController

site = Blueprint('site', __name__)

@site.route('/home', methods=['get'])
def index():
    return SiteController().home();

@site.route('/', methods=['get'])
def home():
    return SiteController().index();