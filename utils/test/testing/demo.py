import os
import io
from datetime import datetime
from flask import Flask, request, url_for, send_from_directory, render_template
import numpy as np
import torch
import torchvision
import torchxrayvision as xrv
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.measure import find_contours

app = Flask(__name__)

# Đường dẫn lưu trữ hình ảnh đã xử lý
PROCESSED_FOLDER = 'static/img'

# Load the model
model = xrv.baseline_models.chestx_det.PSPNet()

@app.route('/', methods=['GET'])
def predict_GET():
    return render_template('demo.html', img_after='../static/img/423472066_698823819127914_2411526179078620117_n.jpg');

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    img = imread(file)

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
        pred = model(img)

    pred = 1 / (1 + np.exp(-pred))  # sigmoid
    pred[pred < 0.5] = 0
    pred[pred > 0.5] = 1

    # Plot the contours on the image
    fig, ax = plt.subplots()
    ax.imshow(img[0, 0], cmap='gray')
    combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)
    target_indices = list(range(14))
    contour_colors = ['red', 'red', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'black',
                      'orange', 'purple', 'green', 'brown', 'gray', 'lime']

    for idx, i in enumerate(target_indices):
        mask = pred[0, i].numpy()
        combined_mask[mask > 0] = idx + 1
        contours = find_contours(combined_mask, level=idx + 0.1)
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], linestyle='--', linewidth=1, color=contour_colors[idx])

    ax.axis('off')

    # Tạo tên file duy nhất bằng timestamp
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
    filepath = os.path.join(PROCESSED_FOLDER, filename)
    plt.savefig(filepath)
    plt.close()

    img_after = url_for('static', filename=f'img/{filename}', _external=True);
    # Trả về URL của hình ảnh đã lưu
    return render_template('demo.html', img_after=img_after);

@app.route('/predict_NEW', methods=['POST'])
def predict_NEW():
    file = request.files['file']
    img = imread(file)
    selected_indices = []

    checkbox = request.form.getlist('checkbox');
    selected_indices = list(map(int, checkbox))
    print(checkbox);
    print(selected_indices);

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
        pred = model(img)

    pred = 1 / (1 + np.exp(-pred))  # sigmoid
    pred[pred < 0.5] = 0
    pred[pred > 0.5] = 1

    # Plot the contours on the image
    fig, ax = plt.subplots()
    ax.imshow(img[0, 0], cmap='gray')
    combined_mask = np.zeros_like(img[0, 0], dtype=np.uint8)

    # Indices for the masks you want to combine
    target_indices = selected_indices  # Indices for left lung, right lung, and heart
    contour_colors = ['red', 'blue', 'green']

    for idx, i in enumerate(target_indices):
        mask = pred[0, i].numpy()
        combined_mask[mask > 0] = idx + 1
        contours = find_contours(combined_mask, level=idx + 0.1)
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], linestyle='--', linewidth=1, color=contour_colors[idx])

    ax.axis('off')

    # Tạo tên file duy nhất bằng timestamp
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
    filepath = os.path.join(PROCESSED_FOLDER, filename)
    plt.savefig(filepath)
    plt.close()

    # Trả về URL của hình ảnh đã lưu
    # return url_for('static', filename=f'img/{filename}', _external=True)
    return render_template('demo.html', img_after=url_for('static', filename=f'img/{filename}', _external=True));

if __name__ == '__main__':
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
