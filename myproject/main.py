
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from skimage.color import lab2rgb, rgb2lab
from model.model import MainModel
from net_gan.train_unet import build_res_unet
from constants import NET_GAN_PATH, MODEL_PATH, SIZE

app = Flask(__name__)
CORS(app)
def load_model():
    net_G = build_res_unet(n_input=1, n_output=2, size=SIZE)
    state_dict = torch.load(NET_GAN_PATH, map_location=torch.device('cpu'))
    net_G.load_state_dict(state_dict)
    model = MainModel(net_G=net_G)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()

def lab_to_rgb(L, ab):
    L = (L + 1.) * 50.
    ab = ab * 110.
    Lab = torch.cat([L, ab], dim=1).permute(0, 2, 3, 1).detach().cpu().numpy()
    rgb_imgs = []
    for img in Lab:
        img_rgb = lab2rgb(img)
        rgb_imgs.append(img_rgb)
    return np.stack(rgb_imgs, axis=0)

def color_image(img_pil, model):
    transforms1 = transforms.Resize((SIZE, SIZE), Image.BICUBIC)
    img = transforms1(img_pil)
    img = np.array(img)
    img_lab = rgb2lab(img).astype("float32")
    img_lab = transforms.ToTensor()(img_lab)
    L = img_lab[[0], ...] / 50. - 1.
    model.L = L.unsqueeze(0)
    with torch.no_grad():
        model()
    L = model.L
    ab = model.fake_color
    rgb = lab_to_rgb(L, ab)[0]
    rgb = np.uint8(rgb * 255)
    return Image.fromarray(rgb)

@app.route('/colorize', methods=['POST'])
def colorize():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    print(f"Received file: {file.filename}")
    img = Image.open(file.stream).convert("RGB")
    print("Image opened, starting colorization...")
    colored_img = color_image(img, model)
    print("Colorization done.")

    img_io = io.BytesIO()
    colored_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(port=5000)



