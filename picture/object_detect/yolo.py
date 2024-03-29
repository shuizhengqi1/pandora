from ultralytics import YOLO
from PIL import Image
import torch
from torchvision.transforms import functional as F

import cv2

local_model_path = "/Users/yanghengxing/PycharmProjects/pandora/model/yolov8x.pt"


def detect(path):
    model = YOLO(local_model_path)
    # 读取图片
    img = Image.open(path)
    # 图片预处理
    # 物体检测
    results = model.predict(source=img, save=True, save_txt=True, conf=0.5)
    # 解析结果
    for i, r in enumerate(results):
        im_bgr = r.plot()  # BGR-order numpy array
        im_rgb = Image.fromarray(im_bgr[..., ::-1])
        #保存到指定的地点
        r.save(filename=f'result-{i}.jpg')


detect("/Users/yanghengxing/Pictures/wallpaa.jpeg")
