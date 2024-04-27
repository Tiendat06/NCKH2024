from database import DataBaseUtils
from flask import redirect

class Disease:

    def __init__(self, disease_id, disease_name, disease_name_eng):
        self.__disease_id = disease_id;
        self.__disease_name = disease_name
        self.__disease_name_eng = disease_name_eng

    @property
    def _disease_id(self):
        return self.__disease_id

    @_disease_id.setter
    def _disease_id(self, value):
        self.__disease_id = value

    @property
    def _disease_name(self):
        return self.__disease_name

    @_disease_name.setter
    def _disease_name(self, value):
        self.__disease_name = value

    @property
    def _disease_name_eng(self):
        return self.__disease_name_eng

    @_disease_name_eng.setter
    def _disease_name_eng(self, value):
        self.__disease_name_eng = value


class DiseaseModel(DataBaseUtils):
    # __conn = DataBaseUtils.get_connection();
    def __init__(self):
        self.__conn = DataBaseUtils.get_connection();
    
    def getAllDisease(self):
        disease_data = self.__conn.get_collection('disease').find();
        data = [];

        if disease_data:
            for disease in disease_data:
                disease_id = disease.get('disease_id');
                disease_name = disease.get('disease_name');
                disease_name_eng = disease.get('disease_name_eng');
                disease_model = Disease(disease_id, disease_name, disease_name_eng);
                data.append(disease_model);
            return data
        return None;
    
    
    def AUTO_DIS_ID(self):
        result = self.__conn.get_collection('disease').find_one({}, sort=[("disease_id", -1)])  #asc

        if result:
            max_dis_id = result['disease_id'];
        else:
            max_dis_id = None;

        if max_dis_id:
            next_dis_id = int(max_dis_id[3:]) + 1
        else:
            next_dis_id = 1

        format_dis_id = f'DIS{next_dis_id:07d}';
        return format_dis_id;

    