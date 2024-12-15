import json
from datetime import datetime
from database import DataBaseUtils
from app.models.Patient import PatientModel
from app.models.User import UserModel

class Chat:
    def __init__(self, chat_id, user_id, patient_id, content):
        self.__chat_id = chat_id
        self.__user_id = user_id
        self.__patient_id = patient_id
        self.__content = content
        self.__created_at = datetime.now()

    @property
    def _chat_id(self):
        return self.__chat_id

    @_chat_id.setter
    def _chat_id(self, value):
        self.__chat_id = value

    @property
    def _user_id(self):
        return self.__user_id

    @_user_id.setter
    def _user_id(self, value):
        self.__user_id = value

    @property
    def _patient_id(self):
        return self.__patient_id

    @_patient_id.setter
    def _patient_id(self, value):
        self.__patient_id = value

    @property
    def _content(self):
        return self.__content

    @_content.setter
    def _content(self, value):
        self.__content = value

class ChatModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils()
        self.patient_model = PatientModel()
        self.user_model = UserModel()

    def insertChat(self, chatData):
        result = self.__conn.get_collection('chat').insert_one(chatData)
        if result.acknowledged:
            return result
        return None

    def getNewestChat(self):
        latest_chat = self.__conn.get_collection('chat').find_one({}, sort=[('created_at', -1)])
        latest_patient_id_chat = latest_chat.get('patient_id')
        return self.getAllPatientChat(latest_patient_id_chat)

    def getNewestChatByUserId(self, user_id):
        chat = self.__conn.get_collection('chat').find_one({'user_id': user_id}, sort=[('created_at', -1)])
        chat_id = chat.get('chat_id')
        user_id = chat.get('user_id')
        patient_id = chat.get('patient_id')
        content = chat.get('content')
        created_at = chat.get('created_at')

        patient_data = self.patient_model.getPatientById(patient_id)
        patient_data['_id'] = str(patient_data['_id'])
        user_data = ''
        if user_id != '':
            user_data = self.user_model.get_user_by_id(user_id)
            user_data['_id'] = str(user_data['_id'])

        data = []
        data.append({
            'chat_id': chat_id,
            'user_id': user_data,
            'patient_id': patient_data,
            'content': content,
            'created_at': created_at.isoformat()
        })

        return data

    def getNewestChatByPatientId(self, patient_id):
        chat = self.__conn.get_collection('chat').find_one({'patient_id': patient_id}, sort=[('created_at', -1)])
        chat_id = chat.get('chat_id')
        user_id = chat.get('user_id')
        patient_id = chat.get('patient_id')
        content = chat.get('content')
        created_at = chat.get('created_at')

        patient_data = self.patient_model.getPatientById(patient_id)
        patient_data['_id'] = str(patient_data['_id'])
        user_data = ''
        if user_id != '':
            user_data = self.user_model.get_user_by_id(user_id)
            user_data['_id'] = str(user_data['_id'])

        data = []
        data.append({
            'chat_id': chat_id,
            'user_id': user_data,
            'patient_id': patient_data,
            'content': content,
            'created_at': created_at.isoformat()
        })

        return data

    def getAllChats(self):
        chats = self.__conn.get_collection('chat').find({}, sort=[('created_at', 1)])
        data = []
        if chats:
            for chat in chats:
                chat_id = chat.get('chat_id')
                user_id = chat.get('user_id')
                patient_id = chat.get('patient_id')
                content = chat.get('content')
                created_at = chat.get('created_at')

                patient_data = self.patient_model.getPatientById(patient_id)
                user_data = ''
                if user_id != '':
                    user_data = self.user_model.get_user_by_id(user_id)
                data.append({
                    'chat_id': chat_id,
                    'user_id': user_data,
                    'patient_id': patient_data,
                    'content': content,
                    'created_at': created_at.isoformat()
                })
                # print(chat)
            return data
        return None

    def getAllPatientChat(self, patient_id):
        chats = self.__conn.get_collection('chat').find({'patient_id': patient_id}, sort=[('created_at', 1)])
        data = []
        if chats:
            for chat in chats:
                chat_id = chat.get('chat_id')
                user_id = chat.get('user_id')
                patient_id = chat.get('patient_id')
                content = chat.get('content')
                created_at = chat.get('created_at')

                patient_data = self.patient_model.getPatientById(patient_id)
                patient_data['_id'] = str(patient_data['_id'])
                user_data = ''
                if user_id != '':
                    user_data = self.user_model.get_user_by_id(user_id)
                    user_data['_id'] = str(user_data['_id'])
                data.append({
                    'chat_id': chat_id,
                    'user_id': user_data,
                    'patient_id': patient_data,
                    'content': content,
                    'created_at': created_at.isoformat()
                })
                # print(chat)
            return (data)
        return None

    
    def AUTO_CHAT_ID(self):
        result = self.__conn.get_collection('chat').find_one({}, sort=[("chat_id", -1)])  # asc

        if result:
            max_chat_id = result['chat_id']
        else:
            max_chat_id = None

        if max_chat_id:
            next_chat_id = max_chat_id + 1
        else:
            next_chat_id = 1

        format_chat_id = next_chat_id
        return format_chat_id