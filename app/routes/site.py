from flask import Blueprint
from controllers.SiteController import SiteController

site = Blueprint('site', __name__)

@site.route('/', methods=['get'])
def index():
    return SiteController().home();