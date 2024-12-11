from database import DataBaseUtils
from flask import redirect, session


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

    @property
    def __id(self):
        return self.___id

    @__id.setter
    def __id(self, value):
        self.___id = value

    @property
    def _username(self):
        return self.__username

    @_username.setter
    def _username(self, value):
        self.__username = value

    @property
    def _password(self):
        return self.__password

    @_password.setter
    def _password(self, value):
        self.__password = value

    @property
    def _acc_id(self):
        return self.__acc_id

    @_acc_id.setter
    def _acc_id(self, value):
        self.__acc_id = value

    @property
    def _role_id(self):
        return self.__role_id

    @_role_id.setter
    def _role_id(self, value):
        self.__role_id = value
    
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

class AccountModel(DataBaseUtils):
    # __conn = DataBaseUtils.get_connection();
    def __init__(self):
        self.__conn = DataBaseUtils()
    
    def checkLogin(self, data):
        acc_email = self.__conn.get_collection('user').find_one({'email': data['email']});
        # account = 
        acc_pwd = self.__conn.get_collection('account').find_one({'acc_id': acc_email['acc_id'], 'password': data['password']});
        role_id = 'ROL0000003';

        if acc_email and acc_pwd and acc_pwd.get('role_id') != 'ROL0000003':
            role_id = acc_pwd.get('role_id');
            return True, role_id;
        return False, role_id;
    
    def updateRoleById(self, acc_id, role_id):
        result = self.__conn.get_collection('account').update_one({'acc_id': acc_id}, {"$set": {'role_id': role_id}})
        if result.modified_count > 0:
            return True;
        return False;


    def updateRole(self, role, acc_id):
        # print(acc_id)
        # print(role)
        role_id = self.__conn.get_collection('role').find_one({'role_name': role}).get('role_id');
        result = self.__conn.get_collection('account').update_one({'acc_id': acc_id}, {"$set": {'role_id': role_id}})
        if result:
            return True
        return False
    
    def checkPwdIsCorrectByUserId(self, acc_id, pwd):
        data = self.__conn.get_collection('account').find_one({'acc_id': acc_id, 'password': pwd});
        if data:
            return True;
        return False;
    
    def updatePwd(self, acc_id, newPwd):
        result = self.__conn.get_collection('account').update_one({'acc_id': acc_id}, {"$set": {'password': newPwd}});
        if result.modified_count > 0:
            return True;
        return False;

    def checkRole(self):
        acc_id = session.get("acc_id");
        account = self.findAccountByAccId(acc_id);
        role_id = account._role_id;
        if role_id == 'ROL0000002':
            return True;
        return False;

    def findAccountByAccId(self, acc_id):
        result = self.__conn.get_collection('account').find_one({'acc_id': acc_id});
        if result:
            account = Account(result['_id'], result['username'], result['password'], result['acc_id'], result['role_id']);
            return account;
        return None;

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

    