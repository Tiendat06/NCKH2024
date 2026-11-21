import json
import os
import posixpath
import threading
import uuid
from datetime import datetime
from io import BytesIO
from random import random
from urllib.parse import urlparse

import cloudinary.uploader
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import torch
import torchvision
import torchxrayvision as xrv
from flask import render_template, session, request, url_for, send_file, send_from_directory, jsonify, current_app
from skimage.io import imread
from werkzeug.utils import secure_filename
from skimage.measure import find_contours

from app.models.Account import AccountModel
from app.models.BodyTarget import BodyTargetModel, get_pspnet
from app.models.Disease import DiseaseModel
from app.models.MedicalRecord import MedicalRecordModel
from app.models.Patient import PatientModel
from app.models.User import UserModel
from my_yolov6 import my_yolov6

matplotlib.use('Agg')  # Sử dụng backend 'Agg' cho matplotlib

# Tiền xử lý chuẩn của torchxrayvision trước khi đưa ảnh vào PSPNet
SEG_TRANSFORM = torchvision.transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(512)
])

# Màu đường viền cho từng bộ phận khi vẽ phân đoạn
CONTOUR_COLORS = ['red', 'red', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'black',
                  'orange', 'purple', 'green', 'brown', 'gray', 'lime']

# /xray/proxy-image chỉ được tải ảnh từ các host này (ngoài ảnh tĩnh của chính server)
PROXY_ALLOWED_HOSTS = {'res.cloudinary.com'}

# Mỗi request tạo một XrayController mới, nên model được nạp một lần cho cả tiến trình và dùng chung
_YOLO_LOCK = threading.Lock()
_YOLO_MODEL = None


def get_yolov6():
    """Trả về YOLOv6 dùng chung; lần gọi đầu tiên mới nạp checkpoint."""
    global _YOLO_MODEL
    with _YOLO_LOCK:
        if _YOLO_MODEL is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            _YOLO_MODEL = my_yolov6(os.path.join(base_dir, "weights", "best_ckpt.pt"), "cpu",
                                    os.path.join(base_dir, "data", "vinbigdata.yaml"), 640, True)
    return _YOLO_MODEL


def safe_upload_name(filename):
    """Tên file an toàn cho ảnh upload: bỏ ký tự đường dẫn và thêm tiền tố ngẫu nhiên để không ghi đè nhau."""
    name = secure_filename(filename or '') or 'upload.png'
    return f"{uuid.uuid4().hex[:12]}_{name}"


class XrayController:
    def __init__(self):
        self.account = AccountModel()
        self.disease = DiseaseModel()
        self.patient = PatientModel()
        self.medicalRecord = MedicalRecordModel()
        self.body_target = BodyTargetModel()
        self.user = UserModel()
        self.yolov6_model = get_yolov6()
        self.PROCESSED_FOLDER = os.path.join('static', 'img', 'body_target')
        self.UPLOAD_FOLDER = os.path.join('static', 'img', 'ratio')
        self.PROCESSED_FOLDER_CONTOURS = os.path.join('static', 'img', 'contours')
        self.UPLOAD_FOLDER_CONTOURS = os.path.join('static', 'img', 'upload_contours')
        # Các thư mục output bị gitignore (chỉ giữ .gitkeep): tự tạo nếu thiếu
        for folder in (self.PROCESSED_FOLDER, self.UPLOAD_FOLDER, self.PROCESSED_FOLDER_CONTOURS,
                       self.UPLOAD_FOLDER_CONTOURS, os.path.join('static', 'img', 'new_body_target'),
                       self.body_target.PROCESSED_FOLDER):
            os.makedirs(folder, exist_ok=True)
        self.model = get_pspnet()

    # [GET, POST] /xray
    def load_data(self, app):
        ndet = 0
        body_list = self.body_target.getAllBodyTarget()
        # Nếu là POST (gửi file)
        if request.method == "POST":
            try:
                # Lấy file gửi lên
                image = request.files['file']
                if image:
                    # Lưu file dưới tên an toàn, không trùng
                    filename = safe_upload_name(image.filename)
                    static_folder_path = os.path.join(app.root_path, 'static')
                    path_to_save = os.path.join(static_folder_path, 'img', filename)
                    path_to_save_local = os.path.join(static_folder_path, 'img', 'data', filename)
                    session['relative_path_to_save_local'] = path_to_save_local

                    session['image_name'] = filename
                    session['relative_path_to_save'] = '/static/img/' + filename
                    session['path_to_save'] = path_to_save
                    session.pop('img_local', None)

                    image.save(path_to_save)

                    frame = cv2.imread(path_to_save)
                    frame, ndet, label_name, percentage, sick_name, sick_name_eng, colors = self.yolov6_model.infer(frame, conf_thres=0.3, iou_thres=0.4)

                    if ndet != 0:
                        disease_list = self.disease.getAllDisease()
                        # lưu hình ảnh kết quả, thu nhỏ còn 330x330
                        cv2.imwrite(path_to_save_local, frame)
                        image_re = cv2.imread(path_to_save_local)
                        resized_image = cv2.resize(image_re, (330, 330))
                        cv2.imwrite(path_to_save_local, resized_image)

                        img_local = '/static/img/data/' + filename
                        session['path_to_save_local'] = img_local

                        # Chuyển đổi mảng NumPy thành định dạng hình ảnh
                        image_data = cv2.imencode('.png', frame)[1].tobytes()

                        res = cloudinary.uploader.upload(image_data)
                        path_ = res['secure_url']
                        print(path_)
                        session['path_predict'] = path_
                        real_percentage = [round(float(p) * 100, 2) for p in percentage]

                        zip_data = list(zip(sick_name, real_percentage, sick_name_eng, colors))
                        doctor_zip_data = zip_data

                        return render_template("index.html", user_image = path_ , body_list=body_list, origin_img = session.get('relative_path_to_save'), user_image_local = img_local, disease_list = disease_list, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres = 0.3,
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray',
                        result_status='detected')
                    else:
                        return render_template('index.html', body_list=body_list, origin_img = session.get('relative_path_to_save'), user_image = '/static/img/' + filename, conf_thres = 0.3,
                        rand = str(random()), msg='Không phát hiện bất thường', ndet = ndet, content = 'index', page = 'xray', result_status='normal')
                else:
                    # Nếu không có file thì yêu cầu tải file
                    return render_template('index.html', body_list=body_list, msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray', result_status='empty')

            except Exception as ex:
                # Lỗi xử lý (đọc ảnh, suy luận, Cloudinary...) phải báo là lỗi, không được hiển thị như "không bệnh"
                print("Error:", ex)
                return render_template('index.html', body_list=body_list, msg='Không xử lý được ảnh', content = 'index', page = 'xray', ndet = ndet, result_status='error')

        else:
            # Nếu là GET thì hiển thị giao diện upload
            return render_template('index.html', body_list=body_list, content = 'index', page = 'xray')

    # [POST, AJAX] /xray/ajax/changeRange
    def load_data_ajax(self, app):
        ndet = 0

        if request.method == "POST":
            try:
                data = request.form

                if data:
                    conf_thres_ajax = float(data.get('range'))
                    path_to_save = session.get('path_to_save')
                    print(path_to_save)

                    frame = cv2.imread(path_to_save)
                    frame, ndet, label_name, percentage, sick_name, sick_name_eng, colors = self.yolov6_model.infer(frame, conf_thres=conf_thres_ajax, iou_thres=0.4)

                    if ndet != 0:
                        path_to_save_local = session.get('relative_path_to_save_local')
                        cv2.imwrite(path_to_save_local, frame)
                        image_re = cv2.imread(path_to_save_local)
                        resized_image = cv2.resize(image_re, (330, 330))
                        cv2.imwrite(path_to_save_local, resized_image)

                        image_name = session.get('image_name')
                        random_string = self.medicalRecord.generate_random_string(8)
                        img_local = '/static/img/data/' + image_name + "?random_string=" + random_string
                        session['img_local'] = img_local

                        real_percentage = [round(float(p) * 100, 2) for p in percentage]

                        zip_data = list(zip(sick_name, real_percentage, sick_name_eng, colors))
                        doctor_zip_data = zip_data

                        return render_template("/xray/change_range.html", origin_img = session.get('relative_path_to_save'), user_image = img_local , user_image_local = img_local, rand = str(random()), percentage = percentage, sick_name = sick_name, conf_thres= conf_thres_ajax,
                        real_percentage = real_percentage, zip_data = zip_data, doctor_zip_data = doctor_zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray',
                        result_status='detected')
                    else:
                        # Không còn box nào: ghi lại ảnh hiện tại (không có box) để giao diện không giữ
                        # ảnh kết quả cũ của ngưỡng thấp hơn, gây mâu thuẫn với thông báo.
                        path_to_save_local = session.get('relative_path_to_save_local')
                        cv2.imwrite(path_to_save_local, cv2.resize(frame, (330, 330)))
                        random_string = self.medicalRecord.generate_random_string(8)
                        user_image = '/static/img/data/' + session.get('image_name') + "?random_string=" + random_string
                        session['img_local'] = user_image
                        return render_template('/xray/change_range.html', user_image = user_image, user_image_local = user_image, origin_img = session.get('relative_path_to_save'), conf_thres= conf_thres_ajax,
                        rand = str(random()), msg='Không phát hiện bất thường', ndet = ndet, content = 'index', page = 'xray', result_status='normal')
                else:
                    # Nếu không có dữ liệu, trả về thông báo lỗi
                    return render_template('/xray/change_range.html', msg='Hãy chọn file để tải lên', ndet = ndet, content = 'index', page = 'xray', result_status='empty')

            except Exception as ex:
                # Lỗi xử lý phải báo là lỗi, không được hiển thị như "không bệnh"
                print("Error:", ex)
                return render_template('/xray/change_range.html', msg='Không xử lý được ảnh', content = 'index', page = 'xray', ndet = ndet, result_status='error')

    # [GET] /xray/proxy-image
    def sendImg(self):
        """Trả ảnh cho nút Download. Chỉ phục vụ ảnh tĩnh của chính server hoặc ảnh trên Cloudinary (chống SSRF)."""
        parsed = urlparse(request.args.get('url', ''))

        # Ảnh kết quả nằm trên chính server (/static/img/...): đọc thẳng từ đĩa, không gọi HTTP.
        # Chuẩn hóa đường dẫn để "img/../.." không thoát ra khỏi static/img.
        if parsed.netloc in ('', request.host) and parsed.path.startswith('/static/'):
            relative = posixpath.normpath(parsed.path[len('/static/'):])
            if not relative.startswith('img/'):
                return jsonify({'error': 'URL ảnh không được phép.'}), 400
            return send_from_directory(current_app.static_folder, relative)

        if parsed.scheme == 'https' and parsed.hostname in PROXY_ALLOWED_HOSTS:
            try:
                response = requests.get(parsed.geturl(), timeout=10)
            except requests.RequestException:
                return jsonify({'error': 'Không tải được ảnh.'}), 502
            if response.status_code != 200:
                return jsonify({'error': 'Không tải được ảnh.'}), 502
            return send_file(BytesIO(response.content), mimetype=response.headers.get('Content-Type', 'image/jpeg'))

        return jsonify({'error': 'URL ảnh không được phép.'}), 400

    # [POST, AJAX] /xray/saveRecord
    def saveRecord(self):
        data = request.get_json()
        patient_id = self.patient.AUTO_PAT_ID()
        patient_name = data.get('name')
        patient_PID = data.get('PID')
        patient_age = data.get('age')
        patient_phone = data.get('phone')
        patient_gender = data.get('gender')
        patient_address = data.get('address')
        patient_dob = data.get('dob')
        patient_email = data.get('email')
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = session.get("user_id")

        medical_record_id = self.medicalRecord.AUTO_MDR_ID()
        img_before = session.get('relative_path_to_save')
        img_last = session.get('path_to_save_local')
        medical_predict = data.get('predict')

        result = {
            'empty': 'Please fill out all fields !',
            'email_not_contain': 'Your email has been contained !',
            'success': 'Add Successfully !',
            'fail': 'Add Failed !',
            'not_checking': 'You must check your image first',
        }

        if not all([patient_name, patient_PID, patient_age, patient_phone, patient_gender, patient_address, patient_dob, patient_email, medical_predict, img_before, img_last]):
            return jsonify(result.get('empty'))

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
            result_patient = self.patient.addPatient(patient)
            if not result_patient:
                return jsonify(result.get('fail'))
        else:
            medical_record['patient_id'] = self.patient.getPatientByPID(patient_PID)['patient_id']

        result_medical_record = self.medicalRecord.addMedicalRecord(medical_record)
        if not result_medical_record:
            return jsonify(result.get('fail'))

        return jsonify(result.get('success'))

    # ---------- Phân đoạn cơ quan (torchxrayvision PSPNet) ----------

    def _segment(self, source):
        """Đọc ảnh (đường dẫn hoặc file upload), tiền xử lý và chạy PSPNet.

        Trả về (img, pred): img là tensor (1, 1, 512, 512) đã tiền xử lý,
        pred là mặt nạ 0/1 dạng numpy (1, 14, 512, 512).
        """
        img = imread(source)
        img = xrv.datasets.normalize(img, 255)
        if img.ndim == 2:          # ảnh xám -> (H, W, 1)
            img = img[:, :, None]
        if img.shape[2] == 4:      # bỏ kênh alpha
            img = img[:, :, :3]
        img = img.transpose((2, 0, 1))
        img = torch.from_numpy(SEG_TRANSFORM(img)).unsqueeze(0)

        with torch.no_grad():
            pred = torch.sigmoid(self.model(img)).numpy()
        pred[pred < 0.5] = 0
        pred[pred > 0.5] = 1
        return img, pred

    def _draw_body_target(self, source, selected_indices):
        """Vẽ đường viền các bộ phận được chọn, lưu PNG và trả về (filename, filepath)."""
        img, pred = self._segment(source)

        fig, ax = plt.subplots()
        ax.imshow(img[0, 0], cmap='gray')
        combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)

        for idx, i in enumerate(selected_indices[:len(CONTOUR_COLORS)]):
            combined_mask[pred[0, i] > 0] = idx + 1
            for contour in find_contours(combined_mask, level=idx + 0.1):
                ax.plot(contour[:, 1], contour[:, 0], linestyle='--', linewidth=1, color=CONTOUR_COLORS[idx])

        ax.axis('off')

        # Tạo tên file duy nhất bằng timestamp
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
        filepath = os.path.join(self.PROCESSED_FOLDER, filename)
        plt.savefig(filepath)
        plt.close()
        return filename, filepath

    def _plot_costophrenic_angles(self, pred, draw_both_sides):
        """Vẽ góc sườn hoành hai bên phổi (mặt nạ 4 = phổi trái, 5 = phổi phải)."""
        combined_mask = np.zeros_like(pred[0, 0], dtype=np.uint8)
        for idx, i in enumerate([4, 5]):
            combined_mask[pred[0, i] > 0] = idx + 1
            for contour in find_contours(combined_mask, level=idx + 0.1):
                if i == 4:
                    corner = np.argmax(contour[:, 1] + contour[:, 0])  # góc dưới phải
                    text_dx, text_dy = -10, -10
                else:
                    corner = np.argmin(contour[:, 1] - contour[:, 0])  # góc dưới trái
                    text_dx, text_dy = 15, -12
                p1 = contour[corner]
                p2 = contour[(corner - 25) % len(contour)]
                p3 = contour[(corner + 25) % len(contour)]
                angle = self.body_target.calculate_angle(p1, p2, p3)
                if draw_both_sides:
                    plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'r-', linewidth=1)
                plt.plot([p1[1], p3[1]], [p1[0], p3[0]], 'r-', linewidth=1)
                mid_x, mid_y = (p1[1] + p3[1]) / 2, (p1[0] + p3[0]) / 2
                plt.text(mid_x + text_dx, mid_y + text_dy, f'{angle:.1f}°', color='r', fontsize=8, ha='center', va='center')

    # [POST, AJAX] /xray/show_body_target
    def show_body_target(self):
        try:
            file = request.files['file']

            # Lấy chỉ số các bộ phận được chọn từ checkbox
            checkbox = request.form.getlist('checkbox')
            selected_indices = []
            if checkbox:
                selected_indices = [int(num_str) for num_str in checkbox[0].split(',') if num_str.isdigit()]

            filename, _ = self._draw_body_target(file, selected_indices)

            # Trả về URL của hình ảnh đã lưu
            return render_template('xray/body_target.html', img_after=url_for('static', filename=f'img/body_target/{filename}', _external=True))

        except Exception as e:
            import traceback
            traceback.print_exc()
            return str(e), 500

    # [POST, AJAX] /xray/upload_ratio
    def uploadRatio(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(self.UPLOAD_FOLDER, safe_upload_name(file.filename))
            file.save(file_path)
            processed_image_path = self.body_target.process_image(file_path)
            return jsonify({"processed_image_url": processed_image_path})

    # [POST, AJAX] /xray/upload_contours
    def uploadContours(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = safe_upload_name(file.filename)
            filepath = os.path.join(self.UPLOAD_FOLDER_CONTOURS, filename)
            file.save(filepath)

            img, pred = self._segment(filepath)

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 2)
            plt.imshow(img[0, 0], cmap='gray')
            plt.axis('off')
            self._plot_costophrenic_angles(pred, draw_both_sides=False)

            plt.tight_layout()
            contour_filename = f'contour_{filename}'
            contour_filepath = os.path.join(self.PROCESSED_FOLDER_CONTOURS, contour_filename)
            plt.savefig(contour_filepath)
            plt.close()

            return jsonify({"processed_image_url": f'/static/img/contours/{contour_filename}'})

    # [POST, FETCH] /xray/combine_body_target
    def combine_body_target(self):
        choice = 0
        checkboxBodyOptions = request.form.get('body-options')
        try:
            body_options = json.loads(checkboxBodyOptions)
        except (TypeError, ValueError):
            return jsonify({'error': 'body-options phải là một mảng JSON.'}), 400
        checkboxFunctionOptions = request.form['function-options']
        if 'file' not in request.files:
            return jsonify({'error': 'Không có tệp nào được gửi.'}), 400
        file = request.files['file']
        file_path = os.path.join('static', 'img', 'new_body_target', safe_upload_name(file.filename))
        file.save(file_path)

        img_link_final = ''
        try:
            if checkboxBodyOptions:
                selected_indices = [int(num_str) for num_str in body_options if num_str.isdigit()]
                img_link_final = self.new_show_body_target(file, selected_indices)

            if checkboxFunctionOptions:
                if 'angle' in checkboxFunctionOptions:
                    img_link_final = self.new_update_contours(img_link_final)
                if 'ratio' in checkboxFunctionOptions:
                    choice = 1
                if 'mediastinum' in checkboxFunctionOptions:
                    choice = 3 if choice == 1 else 2
                if choice != 0:
                    img_link_final = self.new_update_ratio(img_link_final, choice)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'status': 'error', 'error': f'Không xử lý được ảnh: {e}'}), 500

        return jsonify({
            'status': 'success',
            'isAngle': False,
            'bodyOptions': checkboxBodyOptions,
            'functionOptions': checkboxFunctionOptions,
            'img_url': img_link_final
        })

    def new_show_body_target(self, file, selected_indices):
        # Lỗi được ném lên để combine_body_target trả 500, không trả tuple lẫn vào img_url như trước
        _, filepath = self._draw_body_target(file, selected_indices)
        return filepath

    def new_update_ratio(self, filepath, choice):
        img, pred = self._segment(filepath)
        img = img[0]  # (1, 512, 512): kênh 0 để vẽ

        # Đường kính lớn nhất (pixel) của mỗi vùng
        def measure_maximum_diameter(mask):
            max_diameter = 0
            for contour in find_contours(mask, level=0.5):
                diameter = contour[:, 0].max() - contour[:, 0].min()
                max_diameter = max(max_diameter, diameter)
            return max_diameter

        heart_mask = pred[0, 8]
        aorta_mask = pred[0, 9]
        diaphramatica_mask = pred[0, 10]
        media_mask = pred[0, 11]

        heart_max_diameter = measure_maximum_diameter(heart_mask)
        diaphramatica_max_diameter = measure_maximum_diameter(diaphramatica_mask)
        media_max_diameter = measure_maximum_diameter(media_mask)
        aorta_max_diameter = measure_maximum_diameter(aorta_mask)

        heart_contours = find_contours(heart_mask, level=0.5)
        diaphramatica_contours = find_contours(diaphramatica_mask, level=0.5)
        aorta_contours = find_contours(aorta_mask, level=0.5)
        media_contours = find_contours(media_mask, level=0.5)

        def y_center(contours):
            return (contours[0][:, 0].min() + contours[0][:, 0].max()) // 2

        plt.figure(figsize=(6, 6))
        plt.imshow(img[0], cmap='gray')

        # Vẽ đường đo ngang qua tâm của mỗi vùng
        def plot_contour_and_line(contours, max_diameter, color):
            y_c = y_center(contours)
            for contour in contours:
                intersection_points = np.array([point for point in contour if point[0] == y_c])
                if intersection_points.size > 0:
                    x_start = max(0, int(np.min(intersection_points[:, 1])))
                    x_end = min(img.shape[2], int(np.max(intersection_points[:, 1])))
                    plt.axhline(y=y_c, color=color, linestyle='--', linewidth=1, xmin=x_start / img.shape[2],
                                xmax=x_end / img.shape[2])
                    plt.plot([x_start, x_start], [y_c - 5, y_c + 5], color=color, linestyle='--', linewidth=1)
                    plt.plot([x_end, x_end], [y_c - 5, y_c + 5], color=color, linestyle='--', linewidth=1)
                    plt.text(x_start + (x_end - x_start) / 2, y_c - 10, f"{max_diameter} px", color=color,
                             fontsize=8, ha='center')

        if choice in (1, 3):  # tim và cơ hoành
            plot_contour_and_line(heart_contours, heart_max_diameter, 'r')
            plot_contour_and_line(diaphramatica_contours, diaphramatica_max_diameter, 'blue')
        if choice in (2, 3):  # động mạch chủ và trung thất
            plot_contour_and_line(aorta_contours, aorta_max_diameter, 'green')
            plot_contour_and_line(media_contours, media_max_diameter, 'purple')
        plt.axis('off')

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_path = os.path.join(self.UPLOAD_FOLDER, f'{current_time}.png')
        plt.savefig(image_path)
        plt.close()
        print(image_path)
        return image_path

    def new_update_contours(self, filepath):
        img, pred = self._segment(filepath)

        plt.figure(figsize=(18, 9))
        plt.imshow(img[0].numpy().transpose((1, 2, 0)), cmap='gray')
        plt.title('Contours')
        plt.axis('off')
        self._plot_costophrenic_angles(pred, draw_both_sides=True)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        contour_filename = f'contour_{current_time}.png'
        contour_filepath = os.path.join(self.PROCESSED_FOLDER_CONTOURS, contour_filename)
        plt.savefig(contour_filepath)
        plt.close()

        # Trả về đường dẫn của ảnh đã lưu
        return contour_filepath
