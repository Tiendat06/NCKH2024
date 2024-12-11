from flask import Blueprint

chat = Blueprint('chat', __name__)

@chat.route('/chat')
def index():
    pass