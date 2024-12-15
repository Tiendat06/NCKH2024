from app.controllers.ChatController import ChatController

class ChatMiddleware:
    def __init__(self):
        self.chatController = ChatController()

    def index(self):
        return self.chatController.index()

    def handle_user_login(self, PID):
        return self.chatController.handle_user_login(PID)

    def message_to_admin(self, data):
        return self.chatController.message_to_admin(data)

    def message_to_client(self, data):
        return self.chatController.message_to_client(data)

    def click_patient_chat(self, data):
        return self.chatController.click_patient_chat(data)