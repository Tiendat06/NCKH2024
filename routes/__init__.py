# from app import 
from flask import render_template, Blueprint
from routes.site import site
from routes.log import log
from routes.error import error
from routes.xray import xray
from routes.account import account
from routes.user import user
from routes.patient import patient
from routes.chat import chat
def routes(app):
    # @app.route('/', methods=['get'])
    # def index():
    #     return Site.SiteRouter(app)
    app.register_blueprint(error)
    app.register_blueprint(site)
    app.register_blueprint(log)
    app.register_blueprint(xray)
    app.register_blueprint(account)
    app.register_blueprint(user)
    app.register_blueprint(patient)
    app.register_blueprint(chat)

    # Site.SiteRouter(app)
    