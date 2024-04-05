
from database import DataBaseUtils

class MedicalRecord:
    def __init__(self, m_rec_id, patient_id, img_before, img_last, medical_predict, percentage, date_created, doctor_predict):
        self.__m_rec_id = m_rec_id;
        self.__patient_id = patient_id;
        self.__img_before = img_before;
        self.__img_last = img_last;
        self.__medical_predict = medical_predict;
        self.__percentage = percentage;
        self.__date_created = date_created;
        self.__doctor_predict = doctor_predict;
        

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


class MedicalRecordModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils();

    