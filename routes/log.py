from flask import Blueprint, current_app
from app.controllers.LogController import LogController
import os
import pathlib
from google_auth_oauthlib.flow import Flow

log = Blueprint('log', __name__)
# login

# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()

#     return wrapper

# [GET]
@log.route('/log/login_gmail', methods=['get'])
def loginByGoogle():
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "apis", "client_secret.json")

    flow = Flow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
            redirect_uri="http://127.0.0.1:5000/callback"
        )
    return LogController().loginByGoogle(flow)

# [GET]
@log.route('/log/login', methods=['get'])
def login():
    return LogController().login()

# [GET]
@log.route('/callback', methods=['get'])
def callback():
    GOOGLE_CLIENT_ID = '439667677299-6ltpjf671e1cg2kmj3slqlqg2bnkmr91.apps.googleusercontent.com'

    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "apis", "client_secret.json")

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="http://127.0.0.1:5000/callback"
    )
    return LogController().callback(flow, GOOGLE_CLIENT_ID)


@log.route('/protected_area')
# @login_is_required
def protected_area():
    return LogController().protected_area()

# [POST]
@log.route('/log/login', methods=['post'])
def loginPost():
    return LogController().loginPost()

# logout
# [GET]
@log.route('/log/logout', methods=['get'])
def logout():
    return LogController().logout()

# register
# [GET]
@log.route('/log/register', methods=['get'])
def register():
    return LogController().register()

# [POST]
@log.route('/log/register', methods=['post'])
def registerPost():
    global app
    app = current_app
    return LogController().registerPost(app)

@log.route('/log/confirm_email/<token>')
def confirm_email(token):
    # s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return LogController().confirm_email(token)
# log.add_url_rule('/log/login', 'loginPost', LogController.loginPost(), methods=['POST'])
