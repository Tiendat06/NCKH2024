from flask import render_template, session, redirect, request, url_for, current_app
from models.Account import AccountModel
import os
from random import random
import cv2
from my_yolov6 import my_yolov6
import cloudinary.uploader
class XrayController:
    def __init__(self):
        self.account = AccountModel();
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
                    path_to_save = str(os.path.join(static_folder_path, 'img', image.filename))

                    # print(str(path_to_save))

                    image.save(path_to_save)

                    # Convert image to dest size tensor
                    frame = cv2.imread(path_to_save)

                    # frame, ndet, label_name, percentage, sick_name = self.yolov6_model.infer(frame, conf_thres=0.2, iou_thres=0.4)
                    frame, ndet, label_name, percentage, sick_name, sick_name_eng, colors = self.yolov6_model.infer(frame, conf_thres=0.3, iou_thres=0.4)

                    if ndet!=0:
                        cv2.imwrite(path_to_save, frame)

                        # # Trả về kết quả
                        # print("img: ",image)
                        # Chuyển đổi mảng NumPy thành định dạng hình ảnh
                        image_data = cv2.imencode('.png', frame)[1].tobytes()

                        res = cloudinary.uploader.upload(image_data);
                        path_ = res['secure_url'];
                        print(path_)
                        real_percentage = []
                        for i in range(len(percentage)):
                            float_percentage = float((percentage[i])) * 100
                            # print(float_percentage)
                            real_percentage.append((round(float_percentage, 2)))
                            # real_percentage.append(int(percentage[i]))
                        
                        zip_data = zip(sick_name, real_percentage, sick_name_eng, colors);
                        # print(real_percentage)
                        return render_template("index.html", user_image = path_ , rand = str(random()), percentage = percentage, sick_name = sick_name,
                        real_percentage = real_percentage, zip_data = zip_data, msg="Tải file lên thành công", ndet = ndet, label=label_name, content = 'index', page = 'xray')
                    else:
                        return render_template('index.html',user_image = image.filename , 
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
            return render_template('index.html', content = 'index', page = 'xray' , user_image = '/static/img/xray-img-check.png')
        
