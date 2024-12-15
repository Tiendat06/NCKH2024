import json

from flask import jsonify, request, render_template
from app.models.Chat import ChatModel
from app.models.Patient import PatientModel
from app.models.User import UserModel
from utils.utils import JSONEncoder
from datetime import datetime
from bson.json_util import dumps

class ChatService:
    def __init__(self):
        self.chat_model = ChatModel()
        self.patient_model = PatientModel()
        self.user_model = UserModel()

    def index(self):
        patients_data = self.patient_model.getAllPatientSortByLastChat()
        latest_chat = self.chat_model.getNewestChat()
        print(latest_chat[0])
        return {
            'patients_data': patients_data,
            'latest_chat': latest_chat,
        }

    def handleUserLogin(self, PID):
        patient = self.patient_model.getPatientByPID(PID)
        patient_id = patient.get('patient_id')
        patient_chats = self.chat_model.getAllPatientChat(patient_id)
        if patient_chats:
            return {
                'status': True,
                'patient_chats': patient_chats,
                'msg': 'Load patient chat successfully'
            }
        return {
            'status': False,
            'msg': 'Load patient chat failed'
        }


    def messageToClient(self, data):
        patient_id = data['patient_id']
        user_id = data['user_id']
        chat_content = data['chat_content']
        patient_request_id = data['patient_request_id']
        chat_id = self.chat_model.AUTO_CHAT_ID()

        chatData = {
            'chat_id': chat_id,
            'patient_id': patient_id,
            'user_id': user_id,
            'content': chat_content,
            # 'patient_request_id': patient_request_id,
            'created_at': datetime.now()
        }
        result = self.chat_model.insertChat(chatData)

        newestChatByPatientId = self.chat_model.getNewestChatByUserId(user_id)
        if result:
            return {
                'status': True,
                'data': newestChatByPatientId,
                'msg': 'Send message from admin successfully'
            }
        return {
            'status': False,
            'msg': 'Send message from admin failed'
        }

    def messageToAdmin(self, data):
        PID = data['PID']
        message = data['message']
        patient = self.patient_model.getPatientByPID(PID)
        chat_id = self.chat_model.AUTO_CHAT_ID()
        chatData = {
            'chat_id': chat_id,
            'user_id': '',
            'patient_id': patient['patient_id'],
            'content': message,
            'created_at': datetime.now()
        }

        result = self.chat_model.insertChat(chatData)

        patients_data = self.patient_model.getAllPatientSortByLastChat()

        if result:
            return {
                'status': True,
                'patients_data': patients_data,
                'msg': 'Send message from client successfully'
            }
        return {
            'status': False,
            'msg': 'Send message from client failed'
        }

    def clickPatientChat(self, data):
        patient_id = data['patient_id']
        patient_chats = self.chat_model.getAllPatientChat(patient_id)

        if patient_chats:
            return {
                'status': True,
                'patient_chats': patient_chats,
                'msg': 'Load patient chat successfully'
            }
        return {
            'status': False,
            'msg': 'Load patient chat failed'
        }
