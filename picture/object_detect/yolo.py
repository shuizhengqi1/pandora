from ultralytics import YOLO
from PIL import Image
import cv2


def detect(path):
    model = YOLO("../../data/yolov8x-oiv7.pt")
    model.info()
    image = Image.open(path)
    # from PIL
    result = model.predict(image, stream=False, conf=0.5)[0]  # sazve plotted images
    detected_objects = []
    for box in result.boxes:
        detected_objects.append(result.names.get(box[-1].item()))
    print(detected_objects)
    for cls in result.boxes.cls:
        print(f"检测到的名在:{result.names[int(cls.item())]}")

    r.save_crop("./runs")
    print(f"检测到的结果是:{detected_objects}")


detect("/Users/yanghengxing/Pictures/WechatIMG205.jpg")
