from flask import Blueprint, current_app
from app.controllers.XrayController import XrayController

xray = Blueprint('xray', __name__)
app = None

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

@xray.route('/xray/proxy-image', methods=['get'])
def sendImg():
    return XrayController().sendImg();

@xray.route('/xray/saveRecord', methods=['post'])
def saveRecord():
    return XrayController().saveRecord();

@xray.route('/xray/show_body_target', methods=['post'])
def show_body_target():
    return XrayController().show_body_target();

@xray.route('/xray/upload_ratio', methods=['post'])
def upload_ratio():
    return XrayController().uploadRatio();

@xray.route('/xray/upload_contours', methods=['post'])
def upload_contours():
    return XrayController().uploadContours();

@xray.route('/xray/combine_body_target', methods=['post'])
def combine_body_target():
    return XrayController().combine_body_target();