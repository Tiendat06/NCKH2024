from flask import render_template, session, redirect, request, url_for, current_app, sessions, send_file, jsonify
from datetime import datetime
import requests
import random
from io import BytesIO
from models.Account import AccountModel
from models.Disease import DiseaseModel
from models.Patient import PatientModel
from models.MedicalRecord import MedicalRecordModel
from models.User import UserModel
import os
from random import random
import cv2
from my_yolov6 import my_yolov6
import cloudinary.uploader
class XrayController:
    def __init__(self):
        self.account = AccountModel();
        self.disease = DiseaseModel();
        self.patient = PatientModel();
        self.medicalRecord = MedicalRecordModel();
        self.user = UserModel();
        base_dir = os.path.dirname(os.path.abspath(__file__))
        weights_path = os.path.join(base_dir, "weights", "best_ckpt.pt")
        config_path = os.path.join(base_dir, "data", "vinbigdata.yaml")
        self.yolov6_model = my_yolov6(weights_path, "cpu", config_path, 640, True)

    # [GET]
    def index(self):

        return render_template("index.html", content = 'index', page = 'xray')
    
    def load_data(self, app):
        ndet = 0

        # Nếu là POST (gửi file)
        if request.method == "POST":
            # current_path = request.path;
            # print(current_path);
            # path_pt = url_for('static', filename='weights/best_ckpt.pt')
            # print(path_pt);
            # path_yaml = url_for('static', filename='data/vinbigdata.yaml')
            # print(path_yaml)
            # print("YLv6: ", yolov6_model)
            
            try:
                # Lấy file gửi lên
                image = request.files['file']
                if image:
                    # Lưu file
                    # path_save = url_for('static', filename='img')
                    # path_to_save = os.path.join(path_save, image.filename)
                    # res = cloudinary.uploader.upload(image);
                    # path_to_save = res['secure_url'];
                    # print(path_to_save)
                    # print("Path to save:", path_to_save);
                    # print("Save = ", path_to_save)
                    # path_to_save = "../static/img/"+image.filename
                    static_folder_path = os.path.join(app.root_path, 'static')
                    path_to_save = (os.path.join(static_folder_path, 'img', image.filename))
                    path_to_save_local = (os.path.join(static_folder_path, 'img', 'data', image.filename))
                    # image.save(path_to_save_local)
                    session['relative_path_to_save_local'] = path_to_save_local;

                    print((path_to_save))
                    session['image_name'] = image.filename;
                    session['relative_path_to_save'] = '/static/img/'+image.filename
                    session['path_to_save'] = path_to_save

                    image.save(path_to_save)

                    # Convert image to dest size tensor
                    frame = cv2.imread(path_to_save)

                    # frame, ndet, label_name, percentage, sick_name = self.yolov6_model.infer(frame, conf_thres=0.2, iou_thres=0.4)
                    frame, ndet, label_name, percentage, sick_name, sick_name_eng, colors = self.yolov6_model.infer(frame, conf_thres=0.3, iou_thres=0.4)

                    if ndet!=0:

                        disease_list = []
                        disease_list = self.disease.getAllDisease();
                        # lưu hình ảnh
                        # cv2.imwrite(path_to_save, frame)
                        cv2.imwrite(path_to_save_local, frame);

                        # resize img
                        image_re = cv2.imread(path_to_save_local)
                        resized_image = cv2.resize(image_re, (330, 330))
                        cv2.imwrite(path_to_save_local, resized_image)

                        img_local = '/static/img/data/'+image.filename
                        session['path_to_save_local'] = img_local

                        # # Trả về kết quả
                        # print("img: ",image)
                        # Chuyển đổi mảng NumPy thành định dạng hình ảnh
                        image_data = cv2.imencode('.png', frame)[1].tobytes()

                        res = cloudinary.uploader.upload(image_data);
                        path_ = res['secure_url'];
                        print(path_)
                        session['path_predict'] = path_;
                        real_percentage = []
                        for i in range(len(percentage)):
                            float_percentage = float((percentage[i])) * 100
                            # print(float_percentage)
                            real_percentage.append((round(float_percentage, 2)))
                            # real_percentage.append(int(percentage[i]))
                        
                        zip_data = list(zip(sick_name, real_percentage, sick_name_eng, colors));
                        doctor_zip_data = zip_data;
                        # print(real_percentage)
                        return render_template("index.html", user_image = path_ , user_image_local = img_local, disease_list = disease_list, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres = 0.3,
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray')
                    else:
                        return render_template('index.html',user_image = '/static/img/'+ image.filename, conf_thres = 0.3,
                        rand = str(random()), msg='Không nhận diện được bệnh', ndet = ndet, content = 'index', page = 'xray')
                else:
                    # Nếu không có file thì yêu cầu tải file
                    return render_template('index.html', msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray')

            except Exception as ex:
                # Nếu lỗi thì thông báo
                print(ex)
                return render_template('index.html', msg='Không nhận diện được bệnh', content = 'index', page = 'xray', ndet = ndet)

        else:
            # Nếu là GET thì hiển thị giao diện upload
            return render_template('index.html', content = 'index', page = 'xray')    


    # [POST, AJAX]
    def load_data_ajax(self, app):
        ndet = 0

        if request.method == "POST": 
            try:
                data = request.form;
                # image = request.files['file']
                # print(image.filename)
                
                if data:
                    path_ = data.get('img_link');
                    conf_thres_ajax = float(data.get('range'));
                    # print(path_)
                    # print(conf_thres_ajax)
                    # static_folder_path = os.path.join(app.root_path, 'static')
                    # path_to_save = str(os.path.join(static_folder_path, 'img', image.filename))
                    path_to_save = session.get('path_to_save')
                    print(path_to_save)

                    # Tìm đường dẫn tương đối của thư mục static
                    # static_path = os.path.relpath(path_to_save, os.path.join(os.getcwd(), 'app'))

                    path_ = session.get('path_predict');

                    # Convert image to dest size tensor
                    frame = cv2.imread(path_to_save)

                    # frame, ndet, label_name, percentage, sick_name = self.yolov6_model.infer(frame, conf_thres=0.2, iou_thres=0.4)
                    frame, ndet, label_name, percentage, sick_name, sick_name_eng, colors = self.yolov6_model.infer(frame, conf_thres=conf_thres_ajax, iou_thres=0.4)
                    zip_data = []
                    doctor_zip_data = []

                    if ndet!=0:
                        # os.remove(session.get('path_to_save_local'));
                        path_to_save_local = session.get('relative_path_to_save_local');
                        cv2.imwrite(path_to_save_local, frame)

                        image_re = cv2.imread(path_to_save_local)
                        resized_image = cv2.resize(image_re, (330, 330))
                        cv2.imwrite(path_to_save_local, resized_image)

                        image_name = session.get('image_name');
                        random_string = self.medicalRecord.generate_random_string(8);
                        img_local = '/static/img/data/'+image_name+"?random_string="+random_string;


                        real_percentage = []
                        for i in range(len(percentage)):
                            float_percentage = float((percentage[i])) * 100
                            real_percentage.append((round(float_percentage, 2)))
                        
                        # image_data = cv2.imencode('.png', frame)[1].tobytes()
                        
                        # with open('/static/img/image.png', 'wb') as f:
                        #     f.write(image_data)

                        # res = cloudinary.uploader.upload(image_data);
                        # path_ = res['secure_url'];
                        
                        # print(path_)
                        
                        zip_data = list(zip(sick_name, real_percentage, sick_name_eng, colors));
                        doctor_zip_data = zip_data;

                        return render_template("/xray/change_range.html", user_image = img_local , user_image_local = img_local, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres= conf_thres_ajax, 
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray')
                    else:
                        return render_template('/xray/change_range.html',user_image = img_local , conf_thres= conf_thres_ajax,
                        rand = str(random()), msg='Không nhận diện được bệnh', ndet = ndet, content = 'index', page = 'xray')
                else:
                    # Nếu không có dữ liệu, trả về thông báo lỗi
                    return render_template('/xray/change_range.html', msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray')

            except Exception as ex:
                # Ghi log lỗi vào console hoặc tệp log
                print("Error:", ex)
                # Trả về một thông báo lỗi cho client
                return render_template('/xray/change_range.html', msg='Không nhận diện được bệnh', content = 'index', page = 'xray', ndet = ndet)

    # [GET]
    def sendImg(self):
        image_url = request.args.get('url')
        print(image_url)
        response = requests.get(image_url)

        return send_file(BytesIO(response.content), mimetype='image/jpeg')
    
    
    # [POST, AJAX]
    def saveRecord(self):
        data = request.get_json();
        patient_id = self.patient.AUTO_PAT_ID();
        patient_name = data.get('name');
        patient_PID = data.get('PID');
        patient_age = data.get('age');
        patient_phone = data.get('phone');
        patient_gender = data.get('gender');
        patient_address = data.get('address');
        patient_dob = data.get('dob');
        patient_email = data.get('email');
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S");

        medical_record_id = self.medicalRecord.AUTO_MDR_ID();
        img_before = session.get('relative_path_to_save');
        img_last = session.get('path_to_save_local');
        medical_predict = data.get('predict');

        result = {
            'empty': 'Please fill out all fields !',
            'email_not_contain': 'Your email has been contained !',
            'success': 'Add Successfully !',
            'fail': 'Add Failed !',
            'not_checking': 'You must check your image first',
        }     

        if not all([patient_name, patient_PID, patient_age, patient_phone, patient_gender, patient_address, patient_dob, patient_email, medical_predict, img_before, img_last]):
            return jsonify(result.get('empty'));

        patient = {
            'patient_id': patient_id,
            'name': patient_name,
            'age': patient_age,
            'img': '',
            'phone': patient_phone,
            'PID': patient_PID,
            'gender': patient_gender,
            'address': patient_address,
            'date_created': date_created,
            'dob': patient_dob,
            'email': patient_email
        }

        medical_record = {
            'm_rec_id': medical_record_id,
            'patient_id': patient_id,
            'img_before': img_before,
            'img_last': img_last,
            'medical_predict': medical_predict,
            'percentage': '',
            'date_created': date_created,
            'doctor_predict': ''
        }

        if not self.patient.checkPatientIsContainByPID(patient_PID):
            # if self.patient.checkEmailIsContain(patient_email):
                # return jsonify(result.get('email_not_contain'));
            result_patient = self.patient.addPatient(patient);
            if not result_patient:
                return jsonify(result.get('fail'));
        else:
            medical_record['patient_id'] = self.patient.getPatientByPID(patient_PID)['patient_id'];

        
        result_medical_record = self.medicalRecord.addMedicalRecord(medical_record);
        if not result_medical_record:
            return jsonify(result.get('fail'));
        
        return jsonify(result.get('success'));
