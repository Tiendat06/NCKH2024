from flask import Blueprint, Flask, current_app
from controllers.XrayController import XrayController
import os

xray = Blueprint('xray', __name__)
app = None

# [GET]
# @xray.route('/xray', methods=['get'])
# def index():
#     global xray
#     return XrayController().index();

# [GET, POST]
@xray.route('/xray', methods=['post', 'get'])
def load_data():
    global app;
    app = current_app
    print("Current app:",app)
    return XrayController().load_data(app)

# [POST, AJAX]
@xray.route('/xray/ajax/changeRange', methods=['post'])
def load_data_ajax():
    global app;
    app = current_app
    return XrayController().load_data_ajax(app)
