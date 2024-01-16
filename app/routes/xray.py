from flask import Blueprint
from controllers.XrayController import XrayController

xray = Blueprint('xray', __name__)

@xray.route('/xray', methods=['get'])
def index():
    return XrayController().index();
