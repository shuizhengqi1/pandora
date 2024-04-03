import os.path
import json
import numpy as np
import requests
from ultralytics import YOLO
from PIL import Image
from domain import object_detect_db
from domain import base_config_db

download_url = "https://iotxing-1253163150.cos.ap-shanghai.myqcloud.com/yolov8x.pt"

yolo_path = None
yolo_file_name = "yolov8x.pt"


def check_and_download_model():
    global yolo_path
    model_path_json = json.loads(base_config_db.get_config(base_config_db.ConfigKeyEnum.MODEL_PATH.value))
    if model_path_json:
        yolo_path = model_path_json['yolo']
    if not yolo_path:
        raise ValueError("yolo model地址不存在")
    if not os.path.exists(os.path.join(yolo_path, yolo_file_name)):
        print(f"当前yolo模型不存在，准备下载 存储地址:{yolo_path}")
        if not os.path.exists(yolo_path):
            os.makedirs(yolo_path)
        response = requests.get(download_url)
        if response.status_code == 200:
            print(f"开始下载 存储地址:{yolo_path}")
            with open(os.path.join(yolo_path, yolo_file_name), 'wb') as file:
                file.write(response.content)
        else:nn
            print(f"从 {download_url} 下载文件失败，状态码：{response.status_code}")


# yolo中的result是个多维数组，shape的数据是[物体数量,6]或者[物体数量,7]。boxes本身是个对象，由多个数组组成的。
# 通过shape可以获取到数量的信息，通过cls可以获取到名称的信息，但是这里cls里面是个数组，需要用下标去取。conf这些也是一样的。
# 各个数组里面都存储的信息，需要用下标去

def detect(file_path, tmp_save_path):
    model = YOLO(os.path.join(yolo_path, yolo_file_name))
    # 读取图片
    img = Image.open(file_path)
    # 图片预处理
    # 物体检测
    results = model.predict(source=np.array(img), conf=0.5)
    for result in results:
        # 物体总数量
        shape_count = result.boxes.shape[0]
        # 初始化统计字典
        objects_count = {}
        for i in range(shape_count):
            cls_name = result.names[int(result.boxes.cls[i].item())]
            confidence = round(float(result.boxes.conf[i].item()), 2)
            boxes_edge = result.boxes.xyxy[i].tolist()
            boxes_edge = [int(round(coord)) for coord in boxes_edge]
            # 更新物体数量统计
            if cls_name not in objects_count:
                objects_count[cls_name] = 0
            objects_count[cls_name] += 1

            object_img = img.crop(boxes_edge)
            crop_save_path = os.path.join(tmp_save_path, f'{cls_name}_{objects_count[cls_name]}.jpg')
            object_img.save(crop_save_path)

            return object_detect_db.ObjectDetect(
                object_name=cls_name,
                conf=confidence,
                object_detect_db=crop_save_path
            )


check_and_download_model()
