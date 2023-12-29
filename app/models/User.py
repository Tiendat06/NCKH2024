from config import DataBaseUtils

class User:
    # ___id = ''
    # __name = ''
    # __password = ''
    def __init__(self, _id, username, password):
        self.___id = _id;
        self.__name = username
        self.__password = password
    
    def get_userid(self):
        return self.___id;
    
    def get_username(self):
        return self.__name
    
    def get_password(self):
        return self.__password
    
    def set_username(self, username):
        self.__name = username
    
    def set_password(self, password):
        self.__password = password

class UserModel:
    # __conn = DataBaseUtils.get_connection();
    def __init__(self):
        self.__conn = DataBaseUtils.get_connection();

    def get_user(self):
        user_data = self.__conn.get_collection('account').find();
        users_list = []
        if user_data:
            for user in user_data:
                user_id = user.get('_id')
                user_name = user.get('username')
                user_pwd = user.get('password')
                user_model = User(user_id, user_name, user_pwd)
                users_list.append(user_model)
            return users_list;
        return None
    
    def checkLogin(self, data):
        user_email = self.__conn.get_collection('account').find_one({'password': data['password']});
        user_pwd = self.__conn.get_collection('user').find_one({'email': data['email']});
        if user_email and user_pwd:
            return True
        return False
    