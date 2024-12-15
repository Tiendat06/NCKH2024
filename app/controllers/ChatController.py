from flask import render_template
from app.services.ChatService import ChatService

class ChatController:
    def __init__(self):
        self.chatService = ChatService()

    # [GET] /chat
    def index(self):
        data = self.chatService.index()
        return render_template("index.html", content='index', page='chat',
                               patients_data=data['patients_data'], latest_chat=data['latest_chat'])

    def handle_user_login(self, PID):
        return self.chatService.handleUserLogin(PID)

    # websocket
    def message_to_admin(self, data):
        return self.chatService.messageToAdmin(data)

    def message_to_client(self, data):
        return self.chatService.messageToClient(data)

    #websocket
    def click_patient_chat(self, data):
        return self.chatService.clickPatientChat(data)