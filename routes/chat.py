from flask import Blueprint
from app.middlewares.ChatMiddleWare import ChatMiddleware
from app.controllers.ChatController import ChatController

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['get'])
def index():
    return ChatMiddleware().index()