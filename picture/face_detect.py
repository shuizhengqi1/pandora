from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import os
import numpy as np
from tqdm import tqdm
from domain import pic_info_db, face_info_db, file_info_db
from file import file_md5

device = torch.device('cpu')
save_path = './test'
mtcnn = MTCNN(device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

os.makedirs(save_path, exist_ok=True)


def process_all_pic():
    total_count = pic_info_db.get_pic_total_count()
    print(f"当前图片总数为{total_count}")
    unprocessed_count = pic_info_db.get_pic_un_detect_total_count()
    print(f"当前待检测图片总数为{unprocessed_count}")
    total_bar = tqdm(unprocessed_count)
    flag = True
    while flag:
        pic_list = pic_info_db.get_to_process_file_list()
        if not pic_list:
            flag = False
        for pic_info_domain, file_info_domain in pic_list:
            try:
                file_info_domain = check_before_detect(file_info_domain)
                detect_face_and_save(pic_info_domain, file_info_domain)
            except Exception as e:
                print(f"图片{file_info_domain.file_path}检测失败，异常原因:{e}")
            total_bar.update(1)
    total_bar.close()


# 人脸检测之前先判断md5是否存在，如果不存在则处理，然后重新查询
def check_before_detect(file_info: file_info_db.FileInfo):
    if file_info.file_md5 == 'tmp':
        print(f"当前文件{file_info.file_path}md5 不存在，开始计算")
        file_md5.calculate_md5(file_id=file_info.id, file_path=file_info.file_path)
        file_info = file_info_db.get_by_id(file_info.id)
    return file_info


# 检测人脸数据，并保存
def detect_face_and_save(pic_info_domain: pic_info_db.PicInfo, file_info_domain: file_info_db.FileInfo):
    image = Image.open(file_info_domain.file_path)
    # 返回的boxes是包括人脸的框的坐标，points表示的是人脸的五个关键点的坐标,probs是人脸的执行度
    boxes, probs, points = mtcnn.detect(image, landmarks=True)
    face_base_path = os.path.join(save_path, file_info_domain.file_md5)
    # 判断文件夹是否存在，如不存在则创建
    if not os.path.exists(face_base_path):
        os.makedirs(face_base_path)
    if boxes is not None:
        print(f"检测到:{len(boxes)}个人脸")
        for i, (box, point) in enumerate(zip(boxes, points)):
            print(f"处理第{i}个人脸数据")
            # 对获取到的每个人脸进行裁剪
            print(f"开始裁剪")
            face = image.crop(box).convert("RGB")
            face_save_path = os.path.join(face_base_path, f'{i}.png')
            face.save(face_save_path)
            print(f"开始检测人脸特征")
            face_tensor = mtcnn(face)
            if face_tensor is None:
                print(f"未检测到人脸信息 {file_info_domain.file_path}")
                continue
            face_embedding = resnet(face_tensor.unsqueeze(0)).detach().numpy().tobytes()

            face_info_db.add_face_info(face_info_db.FaceInfo(
                pic_id=pic_info_domain.id,
                face_feature=face_embedding,
                face_path=face_save_path,
            ))
        pic_info_domain.face_count = len(boxes)
        pic_info_domain.face_icon_path = face_base_path
        pic_info_db.update_face_detect_result(pic_info_domain)


def check1_embedding(face1, face2):
    # face1_embedding = resnet(mtcnn(face1).unsqueeze(0))
    # face2_embedding = resnet(mtcnn(face2).unsqueeze(0))
    distance = (face1 - face2).norm().item()
    # 设定阈值并判断是否为同一个人
    threshold = 1  # 阈值可以根据实际情况调整
    if distance < threshold:
        print("face1和face2是同一个人")
    else:
        print("face1和face2不是同一个人")

# np_list1 = detect_face_and_save('/Users/yanghengxing/Pictures/WechatIMG205.jpg')
# np_list2 = detect_face_and_save('/Users/yanghengxing/Pictures/WechatIMG206.jpg')
#
# np_list3 = np_list1 + np_list2
# face_list = list(itertools.combinations(np_list3, 2))
# for face_item in face_list:
#     check1_embedding(face_item[0], face_item[1])
# 人脸检测
# 人脸识别
# 人脸特征保存
# 人脸特征对比
# 模型加载
