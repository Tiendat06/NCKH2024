from flask import render_template, session, redirect, request
from models.Account import AccountModel
from models.Patient import Patient, PatientModel
from models.builder.BuilderPatient import BuilderPatient

class SiteController:
    def __init__(self):
        self.account = AccountModel();
        self.patient_model = PatientModel();

    # [GET] /
    def index(self):
        if 'account' not in session:
            return redirect('/home')
        return render_template("index.html", content = 'index', page = 'index')
        
    # [GET] /home
    def home(self):
        if 'account' in session:
            return redirect('/')
        return render_template("index.html", content = 'home');

    # [POST, AJAX] /home/medical_record
    def home_medical_record(self):
        patient_model = self.patient_model;

        data = request.get_json();
        Pid = data.get('Pid');
        print(Pid);
        medical_record_list, user_list = [], [];

        patient = patient_model.getPatientByPID(Pid);
        if patient == None:
            return render_template("/home/home_patient_record.html", patient_name='', medical_record_list=medical_record_list);
        # patient_name = data.get('name');

        medical_record_list, user_list = (patient_model.view_medical_record(patient['patient_id']));

        zip_data = zip(medical_record_list, user_list);
        zip_data_list = list(zip_data)

        # user_list = [];
        # for user in medical_record_list:
        #     user_list.append(user._user_id);

        return render_template("/home/home_patient_record.html", patient_name=patient['name'], medical_record_list=zip_data_list);