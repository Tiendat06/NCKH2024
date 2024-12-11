from flask import request, render_template, jsonify
from app.models.Patient import PatientModel
from app.models.builder.BuilderPatient import BuilderPatient

class PatientController:
    def __init__(self):
        self.patient_model = PatientModel();

    # [GET] /patient
    def index(self, pages):
        patient_db = self.patient_model;
        pages = int(pages);
        per_page = 8;
        start = (pages - 1) * per_page;
        end = start + per_page

        patient_list = []
        patient_list = patient_db.getAllPatient();

        total_pages = (len(patient_list) + per_page - 1) // per_page
        items_on_page = patient_list[start: end]
        return render_template("index.html", content='index', page='patient', patient_list=items_on_page, total_pages=total_pages, pages=pages);

#   [POST] /patient/edit
    def edit_patient(self):
        patient_db = self.patient_model;
        result = {
            'fail': 'Edit failed !',
            'error': 'Your email has been contained !',
            'empty': 'You must to fill out all fields except avatar !',
            'success': 'Edit successfully !'
        }

        data = request.get_json();
        name = data.get('name_edit');
        age = data.get('age_edit');
        phone = data.get('phone_edit');
        Pid = data.get('PID_edit');
        gender = data.get('gender_edit');
        address = data.get('address_edit');
        dob = data.get('dob_edit');
        email = data.get('email_edit');
        date_created = data.get('date_created');
        # img_profile = request.files['file']
        patient_id = data.get('patient_id');
        img = 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png';

        if not all([name, age, Pid, address, date_created, gender, email, dob, phone, patient_id]):
            return jsonify(result.get('empty'))
        
        # patient = Patient(patient_id, name, age, img, phone, Pid, gender, address, date_created, dob, email);
        patient_model = ( 
                    BuilderPatient()
                    .setPatientIdBuilder(patient_id)
                    .setPatientNameBuilder(name)
                    .setPatientAgeBuilder(age)
                    .setPatientImgBuilder(img)
                    .setPatientPhoneBuilder(phone)
                    .setPatientPIDBuilder(Pid)
                    .setPatientGenderBuilder(gender)
                    .setPatientAddressBuilder(address)
                    .setPatientDateCreatedBuilder(date_created)
                    .setPatientDOBBuilder(dob)
                    .setPatientMailBuilder(email)
                    .build()
                );

        if not patient_model:
            return jsonify(result.get('fail'));
        edit = patient_db.edit_patient(patient_model);
        if not edit:
            return jsonify(result.get('fail'));

        return jsonify(result.get('success'));

#   [POST] /patient/delete
    def delete_patient(self):
        patient_model = self.patient_model;
        result = {
            'fail': 'Delete failed !',
            'success': 'Delete successfully !'
        }
        data = request.get_json();
        id = data.get('id');
        patient_data = patient_model.delete_patient(id);
        if not patient_data:
            return jsonify(result.get('fali'));

        return jsonify(result.get('success'));

#   [POST] /patient/medical_record
    def view_medical_record(self):
        patient_model = self.patient_model;
        result = {
            'fail': 'Delete failed !',
            'success': 'Delete successfully !'
        }
        data = request.get_json();
        patient_id = data.get('patient_id');
        patient_name = data.get('name');

        medical_record_list, user_list = [], [];
        medical_record_list, user_list = (patient_model.view_medical_record(patient_id));

        zip_data = zip(medical_record_list, user_list);
        zip_data_list = list(zip_data)

        # user_list = [];
        # for user in medical_record_list:
        #     user_list.append(user._user_id);

        return render_template("/patient/patient_medical_record.html", content='index', page='patient', patient_name=patient_name, medical_record_list=zip_data_list);
