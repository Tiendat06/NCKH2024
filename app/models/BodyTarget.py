from database import DataBaseUtils
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import skimage.io
import os
import torch
import torchvision
import matplotlib.pyplot as plt
import torchxrayvision as xrv
from skimage import measure, transform
from skimage.measure import find_contours
from skimage.transform import resize
from skimage.feature import canny
from skimage.morphology import closing, square
from skimage.io import imread
from flask import render_template, session, redirect, request, url_for, current_app, sessions, send_file, jsonify

class BodyTarget:
    def __init__(self, body_target_id, body_target_name):
        self.__body_target_id = body_target_id 
        self.__body_target_name = body_target_name 

    @property
    def _body_target_id(self):
        return self.__body_target_id

    @_body_target_id.setter
    def _body_target_id(self, value):
        self.__body_target_id = value

    @property
    def _body_target_name(self):
        return self.__body_target_name

    @_body_target_name.setter
    def _body_target_name(self, value):
        self.__body_target_name = value


class BodyTargetModel(DataBaseUtils):
    def __init__(self):
        self.__conn = DataBaseUtils()
        self.model = xrv.baseline_models.chestx_det.PSPNet() 
        self.PROCESSED_FOLDER = 'static/img/upload_ratio' 


    def getAllBodyTarget(self):
        result = self.__conn.get_collection('body_target').find() 
        data = [] 

        if result:
            for body_target in result:
                id = body_target.get('body_target_id') 
                name = body_target.get('body_target_name') 
                body_target_models = BodyTarget(id, name) 
                data.append(body_target_models) 
            return data 
        return None 

    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            print(response.status_code) 
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return np.array(image)  # Convert PIL Image to numpy array
            else:
                print(f"Failed to fetch image from URL. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching image from URL: {e}")
            return None

    def process_image(self, file_path):
        img = skimage.io.imread(file_path)
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
        img = torch.from_numpy(img)

        with torch.no_grad():
            pred = self.model(img.unsqueeze(0))

        pred = 1 / (1 + np.exp(-pred))
        pred[pred < 0.5] = 0
        pred[pred > 0.5] = 1

        def measure_maximum_diameter(mask):
            contours = find_contours(mask, level=0.5)
            max_diameter = 0
            for contour in contours:
                max_y, min_y = contour[:, 0].max(), contour[:, 0].min()
                diameter = max_y - min_y
                if diameter > max_diameter:
                    max_diameter = diameter
            return max_diameter

        left_lung_mask = pred[0, 4].numpy()
        right_lung_mask = pred[0, 5].numpy()
        heart_mask = pred[0, 8].numpy()
        aorta_mask = pred[0, 9].numpy()
        diaphramatica_mask = pred[0, 10].numpy()
        media_mask = pred[0, 11].numpy()

        heart_max_diameter = measure_maximum_diameter(heart_mask)
        lung_combined_mask = np.logical_or(left_lung_mask, right_lung_mask)
        lung_max_diameter = measure_maximum_diameter(lung_combined_mask)
        diaphramatica_max_diameter = measure_maximum_diameter(diaphramatica_mask)
        media_max_diameter = measure_maximum_diameter(media_mask)
        aorta_max_diameter = measure_maximum_diameter(aorta_mask)

        CTR = heart_max_diameter / lung_max_diameter

        heart_contours = find_contours(heart_mask, level=0.5)
        diaphramatica_contours = find_contours(diaphramatica_mask, level=0.5)
        aorta_contours = find_contours(aorta_mask, level=0.5)
        media_contours = find_contours(media_mask, level=0.5)

        heart_x_min, heart_x_max, heart_y_min, heart_y_max = float('inf'), 0, float('inf'), 0
        diaphramatica_x_min, diaphramatica_x_max, diaphramatica_y_min, diaphramatica_y_max = float('inf'), 0, float('inf'), 0
        aorta_x_min, aorta_x_max, aorta_y_min, aorta_y_max = float('inf'), 0, float('inf'), 0
        media_x_min, media_x_max, media_y_min, media_y_max = float('inf'), 0, float('inf'), 0

        for contour in heart_contours:
            x = contour[:, 1]
            y = contour[:, 0]
            heart_x_min = min(heart_x_min, min(x))
            heart_x_max = max(heart_x_max, max(x))
            heart_y_min = min(heart_y_min, min(y))
            heart_y_max = max(heart_y_max, max(y))

        for contour in diaphramatica_contours:
            x = contour[:, 1]
            y = contour[:, 0]
            diaphramatica_x_min = min(diaphramatica_x_min, min(x))
            diaphramatica_x_max = max(diaphramatica_x_max, max(x))
            diaphramatica_y_min = min(diaphramatica_y_min, min(y))
            diaphramatica_y_max = max(diaphramatica_y_max, max(y))

        for contour in media_contours:
            x = contour[:, 1]
            y = contour[:, 0]
            media_x_min = min(media_x_min, min(x))
            media_x_max = max(media_x_max, max(x))
            media_y_min = min(media_y_min, min(y))
            media_y_max = max(media_y_max, max(y))

        for contour in aorta_contours:
            x = contour[:, 1]
            y = contour[:, 0]
            aorta_x_min = min(aorta_x_min, min(x))
            aorta_x_max = max(aorta_x_max, max(x))
            aorta_y_min = min(aorta_y_min, min(y))
            aorta_y_max = max(aorta_y_max, max(y))

        heart_y_center = (heart_y_min + heart_y_max) // 2
        diaphramatica_y_center = (diaphramatica_y_min + diaphramatica_y_max) // 2
        media_y_center = (media_y_min + media_y_max) // 2
        aorta_y_center = (aorta_y_min + aorta_y_max) // 2

        plt.figure(figsize=(6, 6))
        plt.imshow(img[0], cmap='gray')

        for contour in heart_contours:
            intersection_points = np.array([point for point in contour if point[0] == heart_y_center])
            if intersection_points.size > 0:
                x_start = max(0, int(np.min(intersection_points[:, 1])))
                x_end = min(img.shape[2], int(np.max(intersection_points[:, 1])))
                plt.axhline(y=heart_y_center, color='r', linestyle='--', linewidth=1, xmin=x_start/img.shape[2], xmax=x_end/img.shape[2])
                plt.plot([x_start, x_start], [heart_y_center - 5, heart_y_center + 5], color='r', linestyle='--', linewidth=1)
                plt.plot([x_end, x_end], [heart_y_center - 5, heart_y_center + 5], color='r', linestyle='--', linewidth=1)
                plt.text(x_start + (x_end - x_start) / 2, heart_y_center - 10, f"{heart_max_diameter} px", color='r', fontsize=8, ha='center')

        for contour in diaphramatica_contours:
            intersection_points = np.array([point for point in contour if point[0] == diaphramatica_y_center])
            if intersection_points.size > 0:
                x_start = max(0, int(np.min(intersection_points[:, 1])))
                x_end = min(img.shape[2], int(np.max(intersection_points[:, 1])))
                plt.axhline(y=diaphramatica_y_center, color='blue', linestyle='--', linewidth=1, xmin=x_start/img.shape[2], xmax=x_end/img.shape[2])
                plt.plot([x_start, x_start], [diaphramatica_y_center - 5, diaphramatica_y_center + 5], color='blue', linestyle='--', linewidth=1)
                plt.plot([x_end, x_end], [diaphramatica_y_center - 5, diaphramatica_y_center + 5], color='blue', linestyle='--', linewidth=1)
                plt.text(x_start + (x_end - x_start) / 2, diaphramatica_y_center - 10, f"{lung_max_diameter} px", color='blue', fontsize=8, ha='center')

        for contour in aorta_contours:
            intersection_points = np.array([point for point in contour if point[0] == aorta_y_center])
            if intersection_points.size > 0:
                x_start = max(0, int(np.min(intersection_points[:, 1])))
                x_end = min(img.shape[2], int(np.max(intersection_points[:, 1])))
                plt.axhline(y=aorta_y_center, color='green', linestyle='--', linewidth=1, xmin=x_start/img.shape[2], xmax=x_end/img.shape[2])
                plt.plot([x_start, x_start], [aorta_y_center - 5, aorta_y_center + 5], color='green', linestyle='--', linewidth=1)
                plt.plot([x_end, x_end], [aorta_y_center - 5, aorta_y_center + 5], color='green', linestyle='--', linewidth=1)
                plt.text(x_start + (x_end - x_start) / 2, aorta_y_center - 10, f"{aorta_max_diameter} px", color='green', fontsize=8, ha='center')

        for contour in media_contours:
            intersection_points = np.array([point for point in contour if point[0] == media_y_center])
            if intersection_points.size > 0:
                x_start = max(0, int(np.min(intersection_points[:, 1])))
                x_end = min(img.shape[2], int(np.max(intersection_points[:, 1])))
                plt.axhline(y=media_y_center, color='purple', linestyle='--', linewidth=1, xmin=x_start/img.shape[2], xmax=x_end/img.shape[2])
                plt.plot([x_start, x_start], [media_y_center - 5, media_y_center + 5], color='purple', linestyle='--', linewidth=1)
                plt.plot([x_end, x_end], [media_y_center - 5, media_y_center + 5], color='purple', linestyle='--', linewidth=1)
                plt.text(x_start + (x_end - x_start) / 2, media_y_center - 10, f"{media_max_diameter} px", color='purple', fontsize=8, ha='center')

        plt.title(f"Tỉ lệ tim ngực (CTR): {CTR:.2f}")
        plt.axis('off')

        processed_image_path = os.path.join(self.PROCESSED_FOLDER, os.path.basename(file_path))
        plt.savefig(processed_image_path)
        plt.close()

        return processed_image_path 

    def calculate_angle(self, p1, p2, p3):
        vector1 = np.array(p2) - np.array(p1)
        vector2 = np.array(p3) - np.array(p1)
        unit_vector1 = vector1 / np.linalg.norm(vector1)
        unit_vector2 = vector2 / np.linalg.norm(vector2)
        dot_product = np.dot(unit_vector1, unit_vector2)
        angle = np.arccos(dot_product)
        return np.degrees(angle)

    def center_images(self, image):
        threshold = 0.1  # Ngưỡng để xác định pixel không phải màu trắng
        mask = image > threshold

        # Nếu không có pixel nào khác màu trắng, trả lại hình ảnh gốc
        if not np.any(mask):
            return image

        # Tìm bounding box của phần chứa thông tin X-quang
        props = measure.regionprops(measure.label(mask))
        if not props:
            return image  # Không tìm thấy vùng chứa thông tin, trả lại hình ảnh gốc

        largest_region = max(props, key=lambda r: r.area)
        min_row, min_col, max_row, max_col = largest_region.bbox

        # Cắt hình ảnh theo bounding box
        cropped_image = image[min_row:max_row, min_col:max_col]

        # Căn giữa hình ảnh đã cắt
        centered_image = np.zeros_like(image)
        center_row, center_col = image.shape[0] // 2, image.shape[1] // 2
        start_row = max(center_row - cropped_image.shape[0] // 2, 0)
        start_col = max(center_col - cropped_image.shape[1] // 2, 0)
        centered_image[start_row:start_row + cropped_image.shape[0],
        start_col:start_col + cropped_image.shape[1]] = cropped_image

        return centered_image

    def split_image_vertically(self, image_path, output_folder):
        try:
            # Open the local image
            # os.makedirs(output_folder)
            img = Image.open(f'{image_path}')

            # Get image dimensions
            width, height = img.size

            # Calculate the split line
            mid_width = width // 2

            # Crop the image into two halves
            left_half = img.crop((0, 0, mid_width, height))
            right_half = img.crop((mid_width, 0, width, height))

            # Extract the image name and extension from path
            image_name = os.path.basename(image_path)
            name, ext = os.path.splitext(image_name)

            # Save the two halves with the original name
            left_half_path = os.path.join(output_folder, f"{name}_left{ext}")
            right_half_path = os.path.join(output_folder, f"{name}_right{ext}")
            left_half.save(left_half_path)
            right_half.save(right_half_path)

            return left_half_path, right_half_path

        except Exception as e:
            print(f"Error processing the image: {e}")
        return None, None


