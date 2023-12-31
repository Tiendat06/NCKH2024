# from app import 
from flask import render_template, Blueprint
from routes.site import site
from routes.log import log
from routes.error import error

def routes(app):
    # @app.route('/', methods=['get'])
    # def index():
    #     return Site.SiteRouter(app)
    app.register_blueprint(error)
    app.register_blueprint(site)
    app.register_blueprint(log)

    # Site.SiteRouter(app)
    