import json

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
from models.BodyTarget import BodyTargetModel
import os
from random import random
import cv2
from my_yolov6 import my_yolov6
import cloudinary.uploader
import io
from datetime import datetime
import numpy as np
import torch
import torchvision
import torchxrayvision as xrv
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Sử dụng backend 'Agg' cho matplotlib
from skimage.io import imread
from skimage.measure import find_contours
import base64
# from io import BytesIO
from PIL import Image
from datetime import datetime

class XrayController:
    def __init__(self):
        self.account = AccountModel();
        self.disease = DiseaseModel();
        self.patient = PatientModel();
        self.medicalRecord = MedicalRecordModel();
        self.body_target = BodyTargetModel();
        self.user = UserModel();
        base_dir = os.path.dirname(os.path.abspath(__file__));
        weights_path = os.path.join(base_dir, "weights", "best_ckpt.pt");
        config_path = os.path.join(base_dir, "data", "vinbigdata.yaml");
        self.yolov6_model = my_yolov6(weights_path, "cpu", config_path, 640, True);
        self.PROCESSED_FOLDER = os.path.join('static', 'img', 'body_target');# 'static/img/body_target';
        self.UPLOAD_FOLDER = os.path.join('static', 'img', 'ratio'); # 'static/img/ratio';
        self.PROCESSED_FOLDER_CONTOURS = os.path.join('static', 'img', 'contours');# 'static/img/body_target';
        self.UPLOAD_FOLDER_CONTOURS = os.path.join('static', 'img', 'upload_contours'); # 'static/img/ratio';
        self.model = xrv.baseline_models.chestx_det.PSPNet();

    # [GET] 
    def index(self):

        return render_template("index.html", content = 'index', page = 'xray')
    
    # [GET, POST] /xray
    def load_data(self, app):
        ndet = 0
        body_list = [];
        body_list = self.body_target.getAllBodyTarget();
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
                        # height, width, channels = image_re.shape
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

                        return render_template("index.html", user_image = path_ , body_list=body_list, origin_img = session.get('relative_path_to_save'), user_image_local = img_local, disease_list = disease_list, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres = 0.3,
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray')
                    else:
                        return render_template('index.html', body_list=body_list, origin_img = session.get('relative_path_to_save'), user_image = '/static/img/'+ image.filename, conf_thres = 0.3,
                        rand = str(random()), msg='Không nhận diện được bệnh', ndet = ndet, content = 'index', page = 'xray')
                else:
                    # Nếu không có file thì yêu cầu tải file
                    return render_template('index.html', body_list=body_list, msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray')

            except Exception as ex:
                # Nếu lỗi thì thông báo
                print(ex)
                return render_template('index.html', body_list=body_list, msg='Không nhận diện được bệnh', content = 'index', page = 'xray', ndet = ndet)

        else:
            # Nếu là GET thì hiển thị giao diện upload
            return render_template('index.html', body_list=body_list, content = 'index', page = 'xray')    

    # [POST, AJAX] /xray/ajax/changeRange
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

                        image_re = cv2.imread(path_to_save_local);
                        # height, width, channels = image_re.shape

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

                        return render_template("/xray/change_range.html", origin_img = session.get('relative_path_to_save'), user_image = img_local , user_image_local = img_local, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres= conf_thres_ajax, 
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray')
                    else:
                        return render_template('/xray/change_range.html',user_image = img_local , origin_img = session.get('relative_path_to_save'), conf_thres= conf_thres_ajax,
                        rand = str(random()), msg='Không nhận diện được bệnh', ndet = ndet, content = 'index', page = 'xray')
                else:
                    # Nếu không có dữ liệu, trả về thông báo lỗi
                    return render_template('/xray/change_range.html', msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray')

            except Exception as ex:
                # Ghi log lỗi vào console hoặc tệp log
                print("Error:", ex)
                # Trả về một thông báo lỗi cho client
                return render_template('/xray/change_range.html', msg='Không nhận diện được bệnh', content = 'index', page = 'xray', ndet = ndet)

    # [GET] /xray/proxy-image
    def sendImg(self):
        image_url = request.args.get('url')
        print(image_url)
        response = requests.get(image_url)

        return send_file(BytesIO(response.content), mimetype='image/jpeg')
    
    # [POST, AJAX] /xray/saveRecord
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
        user_id = session.get("user_id");

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
            'img': 'https://res.cloudinary.com/dervs0fx5/image/upload/v1709054146/cl0hmsqdjl1lwnahek0i.png',
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
            'doctor_predict': '',
            'user_id': user_id
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

    # [POST, AJAX] /xray/show_body_target
    def show_body_target(self):
        try:
            file = request.files['file']
            img = imread(file)
            
            # Get selected indices from checkboxes
            checkbox = request.form.getlist('checkbox')
            selected_indices = []
            if checkbox:
                str_numbers = checkbox[0].split(',')
                selected_indices = [int(num_str) for num_str in str_numbers if num_str.isdigit()]
            
            # Normalize the image
            img = xrv.datasets.normalize(img, 255)

            # If the image is 2D (grayscale), add an extra dimension to make it (height, width, 1)
            if img.ndim == 2:
                img = img[:, :, None]

            # If the image has 4 channels (RGBA), discard the alpha channel
            if img.shape[2] == 4:
                img = img[:, :, :3]

            # Transpose the image to move the channel dimension to the first position (1, height, width)
            img = img.transpose((2, 0, 1))

            # Apply the transforms
            transform = torchvision.transforms.Compose([
                xrv.datasets.XRayCenterCrop(),
                xrv.datasets.XRayResizer(512)
            ])
            img = transform(img)

            # Convert the image to a PyTorch tensor
            img = torch.from_numpy(img).unsqueeze(0)

            with torch.no_grad():
                pred = self.model(img)

            pred = 1 / (1 + np.exp(-pred))  # sigmoid
            pred[pred < 0.5] = 0
            pred[pred > 0.5] = 1

            # Plot the contours on the image
            fig, ax = plt.subplots()
            ax.imshow(img[0, 0], cmap='gray')
            combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)

            contour_colors = ['red', 'red', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'black',
                            'orange', 'purple', 'green', 'brown', 'gray', 'lime']

            for idx, i in enumerate(selected_indices):
                if idx >= len(contour_colors):
                    break  # Ensure we don't go out of bounds
                mask = pred[0, i].numpy()
                combined_mask[mask > 0] = idx + 1
                contours = find_contours(combined_mask, level=idx + 0.1)
                for contour in contours:
                    ax.plot(contour[:, 1], contour[:, 0], linestyle='--', linewidth=1, color=contour_colors[idx])

            ax.axis('off')

            # Tạo tên file duy nhất bằng timestamp
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
            filepath = os.path.join(self.PROCESSED_FOLDER, filename)
            # print(filepath);
            plt.savefig(filepath)
            # print(filepath)
            plt.close()

            # Trả về URL của hình ảnh đã lưu
            return render_template('xray/body_target.html', img_after=url_for('static', filename=f'img/body_target/{filename}', _external=True))
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            # Handle exceptions and provide feedback
            return str(e), 500

    # [POST, AJAX] /xray/upload_ratio
    def uploadRatio(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(self.UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            processed_image_path = self.body_target.process_image(file_path)
            return jsonify({"processed_image_url": processed_image_path});

    # [POST, AJAX] /xray/upload_contours
    def uploadContours(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            filepath = os.path.join(self.UPLOAD_FOLDER_CONTOURS, filename)
            file.save(filepath)

            # Load and process the image
            img = imread(filepath)
            img = xrv.datasets.normalize(img, 255)
            if img.ndim == 2:
                img = img[:, :, None]
            if img.shape[2] == 4:
                img = img[:, :, :3]
            img = img.transpose((2, 0, 1))

            transform = torchvision.transforms.Compose([
                xrv.datasets.XRayCenterCrop(),
                xrv.datasets.XRayResizer(512)
            ])
            img = transform(img)
            img = torch.from_numpy(img).unsqueeze(0)  # Add batch dimension

            with torch.no_grad():
                pred = self.model(img)

            pred = torch.sigmoid(pred).numpy()
            pred[pred < 0.5] = 0
            pred[pred >= 0.5] = 1

            plt.figure(figsize=(12, 6))
            combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)
            plt.subplot(1, 2, 2)
            plt.imshow(img[0, 0], cmap='gray')
            # plt.title('Contours')
            plt.axis('off')

            target_indices = [4, 5]
            for idx, i in enumerate(target_indices):
                mask = pred[0, i]
                combined_mask[mask > 0] = idx + 1
                contours = find_contours(combined_mask, level=idx + 0.1)
                for contour in contours:
                    if i == 4:
                        bottom_right_idx = np.argmax(contour[:, 1] + contour[:, 0])
                        point1 = contour[bottom_right_idx]
                        point2 = contour[(bottom_right_idx - 25) % len(contour)]
                        point3 = contour[(bottom_right_idx + 25) % len(contour)]
                        angle = self.body_target.calculate_angle(point1, point2, point3)
                        plt.plot([point1[1], point3[1]], [point1[0], point3[0]], 'r-', linewidth=1)
                        mid_x2, mid_y2 = (point1[1] + point3[1]) / 2, (point1[0] + point3[0]) / 2
                        plt.text(mid_x2 - 10, mid_y2 - 10, f'{angle:.1f}°', color='r', fontsize=8, ha='center',
                                 va='center')
                    else:
                        bottom_left_idx = np.argmin(contour[:, 1] - contour[:, 0])
                        point4 = contour[bottom_left_idx]
                        point5 = contour[(bottom_left_idx - 25) % len(contour)]
                        point6 = contour[(bottom_left_idx + 25) % len(contour)]
                        angle = self.body_target.calculate_angle(point4, point5, point6)
                        plt.plot([point4[1], point6[1]], [point4[0], point6[0]], 'r-', linewidth=1)
                        mid_x2, mid_y2 = (point4[1] + point6[1]) / 2, (point4[0] + point6[0]) / 2
                        plt.text(mid_x2 + 15, mid_y2 - 12, f'{angle:.1f}°', color='r', fontsize=8, ha='center',
                                 va='center')

            plt.tight_layout()
            contour_filename = f'contour_{filename}'
            contour_filepath = os.path.join(self.PROCESSED_FOLDER_CONTOURS, contour_filename)
            plt.savefig(contour_filepath)
            plt.close()

            return jsonify({"processed_image_url": f'/static/img/contours/{contour_filename}'})

    # [POST, FETCH] /xray/combine_body_target
    def combine_body_target(self):
        checkboxBodyOptions = request.form.get('body-options');
        checkboxFunctionOptions = request.form['function-options'];
        file = request.files['file'];
        file_path = os.path.join('static', 'img', 'new_body_target', file.filename)
        file.save(file_path)

        img_link_final = '';
        selected_indices = []
        print(json.loads(checkboxBodyOptions))
        # print(checkboxFunctionOptions)
        # print(file_path)
        if 'file' not in request.files:
            return jsonify({'error': 'Không có tệp nào được gửi.'}), 400

        if checkboxBodyOptions:
            # str_numbers = checkboxBodyOptions.split(',')
            # print(str_numbers);
            selected_indices = [int(num_str) for num_str in json.loads(checkboxBodyOptions) if num_str.isdigit()]
            print(selected_indices);
            img_link_final = self.new_show_body_target(file, selected_indices)

        isAngle = False;
        if checkboxFunctionOptions:
            if 'ratio' in checkboxFunctionOptions:
                img_link_final = self.new_upload_ratio(img_link_final);
            if 'angle' in checkboxFunctionOptions:
                isAngle = True;
                img_link_final = self.new_upload_contours(img_link_final, file.filename)

        return jsonify({
            'status': 'success',
            'isAngle': isAngle,
            'bodyOptions': checkboxBodyOptions,
            'functionOptions': checkboxFunctionOptions,
            'img_url': img_link_final
        })

    def new_upload_contours(self, filepath, filename):
        # Load and process the image
        img = imread(filepath)
        img = xrv.datasets.normalize(img, 255)
        if img.ndim == 2:
            img = img[:, :, None]
        if img.shape[2] == 4:
            img = img[:, :, :3]
        img = img.transpose((2, 0, 1))

        transform = torchvision.transforms.Compose([
            xrv.datasets.XRayCenterCrop(),
            xrv.datasets.XRayResizer(512)
        ])
        img = transform(img)
        img = torch.from_numpy(img).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            pred = self.model(img)

        pred = torch.sigmoid(pred).numpy()
        pred[pred < 0.5] = 0
        pred[pred >= 0.5] = 1

        plt.figure(figsize=(12, 6))
        combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)
        plt.subplot(1, 2, 2)
        plt.imshow(img[0, 0], cmap='gray')
        # plt.title('Contours')
        plt.axis('off')

        target_indices = [4, 5]
        for idx, i in enumerate(target_indices):
            mask = pred[0, i]
            combined_mask[mask > 0] = idx + 1
            contours = find_contours(combined_mask, level=idx + 0.1)
            for contour in contours:
                if i == 4:
                    bottom_right_idx = np.argmax(contour[:, 1] + contour[:, 0])
                    point1 = contour[bottom_right_idx]
                    point2 = contour[(bottom_right_idx - 25) % len(contour)]
                    point3 = contour[(bottom_right_idx + 25) % len(contour)]
                    angle = self.body_target.calculate_angle(point1, point2, point3)
                    plt.plot([point1[1], point3[1]], [point1[0], point3[0]], 'r-', linewidth=1)
                    mid_x2, mid_y2 = (point1[1] + point3[1]) / 2, (point1[0] + point3[0]) / 2
                    plt.text(mid_x2 - 10, mid_y2 - 10, f'{angle:.1f}°', color='r', fontsize=8, ha='center',
                             va='center')
                else:
                    bottom_left_idx = np.argmin(contour[:, 1] - contour[:, 0])
                    point4 = contour[bottom_left_idx]
                    point5 = contour[(bottom_left_idx - 25) % len(contour)]
                    point6 = contour[(bottom_left_idx + 25) % len(contour)]
                    angle = self.body_target.calculate_angle(point4, point5, point6)
                    plt.plot([point4[1], point6[1]], [point4[0], point6[0]], 'r-', linewidth=1)
                    mid_x2, mid_y2 = (point4[1] + point6[1]) / 2, (point4[0] + point6[0]) / 2
                    plt.text(mid_x2 + 15, mid_y2 - 12, f'{angle:.1f}°', color='r', fontsize=8, ha='center',
                             va='center')

        plt.tight_layout()
        contour_filename = f'contour_{filename}'
        contour_filepath = os.path.join(self.PROCESSED_FOLDER_CONTOURS, contour_filename)
        plt.savefig(contour_filepath)
        plt.close()

        return contour_filepath;
        # return jsonify({"processed_image_url": f'/static/img/contours/{contour_filename}'})

    def new_upload_ratio(self, filepath):
        processed_image_path = self.body_target.process_image(filepath)
        return processed_image_path;

    def new_show_body_target(self, file, selected_indices):
        try:
            # file = request.files['file']
            img = imread(file)

            # Get selected indices from checkboxes
            # checkbox = request.form.getlist('checkbox')
            # selected_indices = []
            # if checkbox:
            #     str_numbers = checkbox[0].split(',')
            #     selected_indices = [int(num_str) for num_str in str_numbers if num_str.isdigit()]

            # Normalize the image
            img = xrv.datasets.normalize(img, 255)

            # If the image is 2D (grayscale), add an extra dimension to make it (height, width, 1)
            if img.ndim == 2:
                img = img[:, :, None]

            # If the image has 4 channels (RGBA), discard the alpha channel
            if img.shape[2] == 4:
                img = img[:, :, :3]

            # Transpose the image to move the channel dimension to the first position (1, height, width)
            img = img.transpose((2, 0, 1))

            # Apply the transforms
            transform = torchvision.transforms.Compose([
                xrv.datasets.XRayCenterCrop(),
                xrv.datasets.XRayResizer(512)
            ])
            img = transform(img)

            # Convert the image to a PyTorch tensor
            img = torch.from_numpy(img).unsqueeze(0)

            with torch.no_grad():
                pred = self.model(img)

            pred = 1 / (1 + np.exp(-pred))  # sigmoid
            pred[pred < 0.5] = 0
            pred[pred > 0.5] = 1

            # Plot the contours on the image
            fig, ax = plt.subplots()
            ax.imshow(img[0, 0], cmap='gray')
            combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)

            contour_colors = ['red', 'red', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'black',
                              'orange', 'purple', 'green', 'brown', 'gray', 'lime']

            for idx, i in enumerate(selected_indices):
                if idx >= len(contour_colors):
                    break  # Ensure we don't go out of bounds
                mask = pred[0, i].numpy()
                combined_mask[mask > 0] = idx + 1
                contours = find_contours(combined_mask, level=idx + 0.1)
                for contour in contours:
                    ax.plot(contour[:, 1], contour[:, 0], linestyle='--', linewidth=1, color=contour_colors[idx])

            ax.axis('off')

            # Tạo tên file duy nhất bằng timestamp
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
            filepath = os.path.join(self.PROCESSED_FOLDER, filename)
            # print(filepath);
            plt.savefig(filepath)
            # print(filepath)
            plt.close()

            # Trả về URL của hình ảnh đã lưu
            return filepath;
            # return render_template('xray/body_target.html',
            #                        img_after=url_for('static', filename=f'img/body_target/{filename}', _external=True))

        except Exception as e:
            import traceback
            traceback.print_exc()
            # Handle exceptions and provide feedback
            return str(e), 500