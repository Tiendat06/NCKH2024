from database import DataBaseUtils
from flask import request

class Patient():
    def __init__(self, patient_id, name, age, img, phone, PID, gender, address, date_created, dob):
        self.__patient_id = patient_id;
        self.__name = name;
        self.__age = age;
        self.__img = img;
        self.__phone = phone;
        self.__PID = PID;
        self.__gender = gender;
        self.__address = address;
        self.__date_created = date_created;
        self.__dob = dob;

    @property
    def _patient_id(self):
        return self.__patient_id

    @_patient_id.setter
    def _patient_id(self, value):
        self.__patient_id = value

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, value):
        self.__name = value

    @property
    def _age(self):
        return self.__age

    @_age.setter
    def _age(self, value):
        self.__age = value

    @property
    def _img(self):
        return self.__img

    @_img.setter
    def _img(self, value):
        self.__img = value

    @property
    def _phone(self):
        return self.__phone

    @_phone.setter
    def _phone(self, value):
        self.__phone = value

    @property
    def _PID(self):
        return self.__PID

    @_PID.setter
    def _PID(self, value):
        self.__PID = value

    @property
    def _gender(self):
        return self.__gender

    @_gender.setter
    def _gender(self, value):
        self.__gender = value

    @property
    def _address(self):
        return self.__address

    @_address.setter
    def _address(self, value):
        self.__address = value

    @property
    def _date_created(self):
        return self.__date_created

    @_date_created.setter
    def _date_created(self, value):
        self.__date_created = value

    @property
    def _dob(self):
        return self.__dob

    @_dob.setter
    def _dob(self, value):
        self.__dob = value


class PatientModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils();

    def getPatientByPID(self, id):
        data = []
        result = self.__conn.get_collection('patient').find_one({'patient_id': id});
        if result:
            data.append(result);
            return data;
        return None;

    def getAllPatient(self):
        data = []

        patient_data = self.__conn.get_collection('patient').find();

        if patient_data:
            for patient in patient_data:
                id = patient.get('patient_id');
                name = patient.get('name');
                age = patient.get('age');
                img = patient.get('img');
                phone = patient.get('phone');
                PIDs = patient.get('PID');
                gender = patient.get('gender');
                address = patient.get('address');
                date_created = patient.get('date_created');
                dob = patient.get('dob');

                patient_item = Patient(id, name, age, img, phone, PIDs, gender, address, date_created, dob);

                data.append(patient_item)
            return data;
        return data;

