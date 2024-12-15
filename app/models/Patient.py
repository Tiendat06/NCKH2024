from database import DataBaseUtils
from app.models.builder.BuilderPatient import BuilderPatient
from app.models.MedicalRecord import MedicalRecord
from app.models.User import UserModel, User
from datetime import datetime
from pymongo import DESCENDING
class Patient():
    def __init__(self, patient_id, name, age, img, phone, PID, gender, address, date_created, dob, email):
        self.__patient_id = patient_id 
        self.__name = name 
        self.__age = age 
        self.__img = img 
        self.__phone = phone 
        self.__PID = PID 
        self.__gender = gender 
        self.__address = address 
        self.__date_created = date_created 
        self.__dob = dob 
        self.__email = email

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

    @property
    def _email(self):
        return self.__email

    @_email.setter
    def _email(self, value):
        self.__email = value


class PatientModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils()
        self.__user_db = UserModel()
    
    def addPatient(self, patient: Patient):
        result = self.__conn.get_collection('patient').insert_one(patient)
        if result.acknowledged:
            return True
        return False

    def checkPatientIsContainByPID(self, PID):
        result = self.__conn.get_collection('patient').find_one({'PID': PID})
        if result:
            return True
        return False

    def getPatientByPID(self, PID):
        result = self.__conn.get_collection('patient').find_one({'PID': PID}) 
        if result:
            return result 
        return None 

    def edit_patient(self, patient: Patient):
        result = self.__conn.get_collection('patient').update_one({'patient_id': patient._patient_id}, 
                                                               {"$set": { 
                                                                   'name': patient._name,
                                                                   'age': patient._age,
                                                                   'phone': patient._phone,
                                                                   'PID': patient._PID,
                                                                   'gender': patient._gender,
                                                                   'address': patient._address,
                                                                   'dob': patient._dob,
                                                                   'email': patient._email,
                                                                }})
        if result.acknowledged and result.matched_count > 0:
            return True
        return False
    
    def delete_patient(self):
        pass

    def view_medical_record_by_PID(self, PID):
        medical_record_data = self.__conn.get_collection('medical_record').find({'PID': PID}) 
        data = [] 
        user_list = [] 
        if medical_record_data:
            for medical_record in medical_record_data:
                m_rec_id = medical_record.get('m_rec_id')
                patient_id = medical_record.get('patient_id')
                img_before = medical_record.get('img_before') 
                img_last = medical_record.get('img_last') 
                medical_predict = medical_record.get('medical_predict') 
                percentage = medical_record.get('percentage') 
                date_created = medical_record.get('date_created') 
                doctor_predict = medical_record.get('doctor_predict') 
                user_id = medical_record.get('user_id') 

                user = self.__user_db.get_user_by_id(user_id) 

                user_model = User('', user_id, user['acc_id'], user['name'], user['gender'], user['email'], user['dob'], user['phone'], user['img_profile']) 
                medical_record_model = MedicalRecord(m_rec_id, patient_id, img_before, img_last, medical_predict, percentage, date_created, doctor_predict, user_id) 
                data.append(medical_record_model) 
                user_list.append(user_model) 
            return data, user_list 
        return None 

    def view_medical_record(self, patient_id):
        medical_record_data = self.__conn.get_collection('medical_record').find({'patient_id': patient_id}) 
        data = [] 
        user_list = [] 
        if medical_record_data:
            for medical_record in medical_record_data:
                m_rec_id = medical_record.get('m_rec_id') 
                img_before = medical_record.get('img_before') 
                img_last = medical_record.get('img_last') 
                medical_predict = medical_record.get('medical_predict') 
                percentage = medical_record.get('percentage') 
                date_created = medical_record.get('date_created') 
                doctor_predict = medical_record.get('doctor_predict') 
                user_id = medical_record.get('user_id') 

                user = self.__user_db.get_user_by_id(user_id) 

                user_model = User('', user_id, user['acc_id'], user['name'], user['gender'], user['email'], user['dob'], user['phone'], user['img_profile']) 
                medical_record_model = MedicalRecord(m_rec_id, patient_id, img_before, img_last, medical_predict, percentage, date_created, doctor_predict, user_id) 
                data.append(medical_record_model) 
                user_list.append(user_model) 
            return data, user_list 
        return None 


    def getAllPatient(self):
        patient_data = self.__conn.get_collection('patient').find() 
        data = []

        # acc_data = self.__conn.get_collection('account').find() 
        if patient_data:
            for patient in patient_data:
                id = patient.get('patient_id') 
                name = patient.get('name') 
                age = patient.get('age') 
                img = patient.get('img') 
                phone = patient.get('phone') 
                PIDs = patient.get('PID') 
                gender = patient.get('gender') 
                address = patient.get('address') 
                date_created = patient.get('date_created') 
                dob = patient.get('dob') 
                email = patient.get('email')
                # print(id)

                # patient_item = Patient(id, name, age, img, phone, PIDs, gender, address, date_created, dob, email) 
                # BUILDER PATTERN FOR PATIENT [TTD]
                patient_model = ( 
                    BuilderPatient()
                    .setPatientIdBuilder(id)
                    .setPatientNameBuilder(name)
                    .setPatientAgeBuilder(age)
                    .setPatientImgBuilder(img)
                    .setPatientPhoneBuilder(phone)
                    .setPatientPIDBuilder(PIDs)
                    .setPatientGenderBuilder(gender)
                    .setPatientAddressBuilder(address)
                    .setPatientDateCreatedBuilder(date_created)
                    .setPatientDOBBuilder(dob)
                    .setPatientMailBuilder(email)
                    .build()
                ) 

                data.append(patient_model)
            return data 
        return None

    def getAllPatientSortByLastChat(self):
        pipeline = [
            # Lookup để kết nối bảng Chat và Patient
            {
                "$lookup": {
                    "from": "patient",  # Tên collection Patient
                    "localField": "patient_id",  # Trường ở Chat
                    "foreignField": "patient_id",  # Trường ở Patient
                    "as": "patient_info",  # Kết quả gắn vào patient_info
                }
            },
            # Giải nén dữ liệu từ patient_info
            {"$unwind": "$patient_info"},
            # Sắp xếp theo created_at trong Chat giảm dần
            {"$sort": {"created_at": -1}},
            # Nhóm dữ liệu theo patient_id
            {
                "$group": {
                    "_id": "$patient_id",  # Nhóm theo patient_id
                    "latest_chat": {"$first": "$created_at"},  # Giữ thời gian chat mới nhất
                    "chat_content": {"$first": "$content"},  # Lấy nội dung chat mới nhất
                    "patient_details": {"$first": "$patient_info"},  # Lấy thông tin bệnh nhân
                }
            },
            # Sử dụng $project để định dạng datetime
            {
                "$project": {
                    "_id": 0,
                    "patient_id": "$_id",
                    "name": "$patient_details.name",
                    "age": "$patient_details.age",
                    "img": "$patient_details.img",
                    "phone": "$patient_details.phone",
                    "PID": "$patient_details.PID",
                    "gender": "$patient_details.gender",
                    "address": "$patient_details.address",
                    "dob": "$patient_details.dob",
                    "email": "$patient_details.email",
                    "latest_chat": {
                        "$dateToString": {
                            "format": "%Y-%m-%dT%H:%M:%S.%LZ",
                            "date": "$latest_chat",
                        }
                    },
                    "chat_content": "$chat_content",
                }
            },
            # Sắp xếp kết quả theo thời gian chat mới nhất
            {"$sort": {"latest_chat": -1}},
        ]

        # Thực thi pipeline
        result = list(self.__conn.get_collection('chat').aggregate(pipeline))
        # for chat in self.__conn.get_collection('chat').find():
        #     print(chat)
        # for patient in self.__conn.get_collection('patient').find():
        #     print(patient)

        # print(result)
        return result

    def getPatientById(self, patient_id):
        patient_data = self.__conn.get_collection('patient').find_one({'patient_id': patient_id})
        if patient_data:
            return patient_data
        return None

    def loginPatient(self, PID):
        result = self.__conn.get_collection('patient').find_one({'PID': PID})
        if result:
            return result
        return None

    def AUTO_PAT_ID(self):
        result = self.__conn.get_collection('patient').find_one({}, sort=[("patient_id", -1)])  #desc

        if result:
            max_patient_id = result['patient_id'] 
        else:
            max_patient_id = None 

        if max_patient_id:
            next_patient_id = int(max_patient_id[3:]) + 1
        else:
            next_patient_id = 1

        format_patient_id = f'PAT{next_patient_id:07d}' 
        return format_patient_id     