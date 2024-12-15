
from database import DataBaseUtils
import random
import string

class MedicalRecord:
    def __init__(self, m_rec_id, patient_id, img_before, img_last, medical_predict, percentage, date_created, doctor_predict, user_id):
        self.__m_rec_id = m_rec_id 
        self.__patient_id = patient_id 
        self.__img_before = img_before 
        self.__img_last = img_last 
        self.__medical_predict = medical_predict 
        self.__percentage = percentage 
        self.__date_created = date_created 
        self.__doctor_predict = doctor_predict 
        self.__user_id = user_id 

    @property
    def _m_rec_id(self):
        return self.__m_rec_id

    @_m_rec_id.setter
    def _m_rec_id(self, value):
        self.__m_rec_id = value

    @property
    def _patient_id(self):
        return self.__patient_id

    @_patient_id.setter
    def _patient_id(self, value):
        self.__patient_id = value

    @property
    def _img_before(self):
        return self.__img_before

    @_img_before.setter
    def _img_before(self, value):
        self.__img_before = value

    @property
    def _img_last(self):
        return self.__img_last

    @_img_last.setter
    def _img_last(self, value):
        self.__img_last = value

    @property
    def _medical_predict(self):
        return self.__medical_predict

    @_medical_predict.setter
    def _medical_predict(self, value):
        self.__medical_predict = value

    @property
    def _percentage(self):
        return self.__percentage

    @_percentage.setter
    def _percentage(self, value):
        self.__percentage = value

    @property
    def _date_created(self):
        return self.__date_created

    @_date_created.setter
    def _date_created(self, value):
        self.__date_created = value

    @property
    def _doctor_predict(self):
        return self.__doctor_predict

    @_doctor_predict.setter
    def _doctor_predict(self, value):
        self.__doctor_predict = value

    @property
    def _user_id(self):
        return self.__user_id

    @_user_id.setter
    def _user_id(self, value):
        self.__user_id = value


class MedicalRecordModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils() 

    def addMedicalRecord(self, medicalRecord):
        result = self.__conn.get_collection('medical_record').insert_one(medicalRecord) 
        if result.acknowledged:
            return True 
        return False 

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def AUTO_MDR_ID(self):
        result = self.__conn.get_collection('medical_record').find_one({}, sort=[("m_rec_id", -1)])  #desc

        if result:
            max_medical_id = result['m_rec_id'] 
        else:
            max_medical_id = None 

        if max_medical_id:
            next_medical_id = int(max_medical_id[3:]) + 1
        else:
            next_medical_id = 1

        format_medical_id = f'MDR{next_medical_id:07d}' 
        return format_medical_id     
    