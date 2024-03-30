from ultralytics import YOLO
from PIL import Image

local_model_path = "C:\\Users\shuiz\Downloads\yolov8x.pt"


# yolo中的result是个多维数组，shape的数据是[物体数量,6]或者[物体数量,7]。boxes本身是个对象，由多个数组组成的。
# 通过shape可以获取到数量的信息，通过cls可以获取到名称的信息，但是这里cls里面是个数组，需要用下标去取。conf这些也是一样的。
# 各个数组里面都存储的信息，需要用下标去

def detect(path):
    model = YOLO(local_model_path)
    # 读取图片
    img = Image.open(path)
    # 图片预处理
    # 物体检测
    results = model.predict(source=img, conf=0.5)
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
            print(f'物体:{cls_name} 置信度:{confidence}')
            object_img = img.crop(boxes_edge)
            object_img.save(f'{cls_name}_{objects_count[cls_name]}.jpg')


detect("J:\work\memory\\20151004_051237466_iOS.jpg")
