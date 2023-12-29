from config import DataBaseUtils
from models.Account import AccountModel
class User:
    def __init__(self, _id, user_id, acc_id, name, gender, email, dob, phone):
        self.___id = _id;
        self.__user_id = user_id;
        self.__acc_id = acc_id;
        self.__name = name;
        self.__gender = gender;
        self.__email = email;
        self.__dob = dob;
        self.__phone = phone;
    
    @property
    def __id(self):
        return self.___id

    @__id.setter
    def __id(self, value):
        self.___id = value

    @property
    def _user_id(self):
        return self.__user_id

    @_user_id.setter
    def _user_id(self, value):
        self.__user_id = value

    @property
    def _acc_id(self):
        return self.__acc_id

    @_acc_id.setter
    def _acc_id(self, value):
        self.__acc_id = value

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, value):
        self.__name = value

    @property
    def _gender(self):
        return self.__gender

    @_gender.setter
    def _gender(self, value):
        self.__gender = value

    @property
    def _email(self):
        return self.__email

    @_email.setter
    def _email(self, value):
        self.__email = value

    @property
    def _dob(self):
        return self.__dob

    @_dob.setter
    def _dob(self, value):
        self.__dob = value

    @property
    def _phone(self):
        return self.__phone

    @_phone.setter
    def _phone(self, value):
        self.__phone = value

class UserModel:
    def __init__(self):
        self.__conn = DataBaseUtils();

    def add_user(self, user, account):
        user_id = self.AUTO_USE_ID();
        acc_id = AccountModel().AUTO_ACC_ID();
        user_json = {
            'user_id': user_id,
            'acc_id': acc_id,
            'name': user._name,
            'gender': user._gender,
            'email': user._email,
            'dob': user._dob,
            'phone': user._phone
        }

        account_json = {
            'password': account.get_password(),
            'acc_id': acc_id,
            'username': account.get_username(),
            'role_id': account.get_role_id(),
        }
        result_acc = self.__conn.get_collection('account').insert_one(account_json);
        result_user = self.__conn.get_collection('user').insert_one(user_json);


        if result_user.acknowledged and result_acc.acknowledged:
            return 'Add Successfully';
        return 'Add Failed';

    def AUTO_USE_ID(self):
        result = self.__conn.get_collection('user').find_one({}, sort=[("user_id", -1)])  #asc

        if result:
            max_user_id = result['user_id'];
        else:
            max_user_id = None;

        if max_user_id:
            next_user_id = int(max_user_id[3:]) + 1
        else:
            next_user_id = 1

        format_user_id = f'USE{next_user_id:07d}';
        return format_user_id;
        