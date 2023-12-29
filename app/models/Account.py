from config import DataBaseUtils

class Account:
    # ___id = ''
    # __name = ''
    # __password = ''
    def __init__(self, _id, username, password, acc_id, role_id):
        self.___id = _id;
        self.__username = username
        self.__password = password
        self.__acc_id = acc_id
        self.__role_id = role_id;
    
    def get_userid(self):
        return self.___id;
    
    def get_username(self):
        return self.__username
    
    def get_acc_id(self):
        return self.__acc_id;
    
    def get_role_id(self):
        return self.__role_id
    
    def get_password(self):
        return self.__password
    
    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password

class AccountModel:
    # __conn = DataBaseUtils.get_connection();
    def __init__(self):
        self.__conn = DataBaseUtils.get_connection();

    def get_account(self):
        acc_data = self.__conn.get_collection('account').find();
        acc_list = []
        if acc_data:
            for acc in acc_data:
                _id = acc.get('_id')
                acc_name = acc.get('username')
                acc_pwd = acc.get('password')
                acc_id = acc.get('acc_id')
                role_id = acc.get('role_id')
                acc_model = Account(_id, acc_name, acc_pwd, acc_id, role_id)
                acc_list.append(acc_model)
            return acc_list;
        return None
    
    def checkLogin(self, data):
        acc_email = self.__conn.get_collection('account').find_one({'password': data['password']});
        acc_pwd = self.__conn.get_collection('user').find_one({'email': data['email']});
        if acc_email and acc_pwd:
            return True
        return False
    
    def AUTO_ACC_ID(self):
        result = self.__conn.get_collection('account').find_one({}, sort=[("acc_id", -1)])  #asc

        # max_acc_id = result['acc_id'] if result and 'acc_id' in result else None;
        if result:
            max_acc_id = result['acc_id'];
        else:
            max_acc_id = None;

        if max_acc_id:
            next_acc_id = int(max_acc_id[3:]) + 1
        else:
            next_acc_id = 1

        format_acc_id = f'ACC{next_acc_id:07d}';
        return format_acc_id;

    