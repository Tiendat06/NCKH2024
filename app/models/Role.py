from config import DataBaseUtils;
class Role:
    def __init__(self, _id, role_id, role_name):
        self.___id = _id;
        self.__role_id = role_id;
        self.__role_name = role_name;

    @property
    def __id(self):
        return self.___id

    @__id.setter
    def __id(self, value):
        self.___id = value

    @property
    def _role_id(self):
        return self.__role_id

    @_role_id.setter
    def _role_id(self, value):
        self.__role_id = value

    @property
    def _role_name(self):
        return self.__role_name

    @_role_name.setter
    def _role_name(self, value):
        self.__role_name = value

class RoleModel:
    def __init__(self):
        self.__conn = DataBaseUtils();

    def AUTO_ROL_ID(self):
        result = self.__conn.get_collection('role').find_one({}, sort=[("role_id", -1)])  #asc

        if result:
            max_role_id = result['role_id'];
        else:
            max_role_id = None;

        if max_role_id:
            next_role_id = int(max_role_id[3:]) + 1
        else:
            next_role_id = 1

        format_role_id = f'ROL{next_role_id:07d}';
        return format_role_id;
