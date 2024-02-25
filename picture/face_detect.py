from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import shutil
import os
import numpy as np
from tqdm import tqdm
from domain import pic_info_db, face_info_db, file_info_db
from file import file_md5
import concurrent.futures
from queue import Queue

device = torch.device('cuda')
save_path = 'face_icon'
mtcnn = MTCNN(device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().cuda(device)
# 检测用的线程池
detect_executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
# 数据保存用的线程池
save_executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
# cuda信息检测
print(f"torch支持的版本cuda版本是{torch.version.cuda}")
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")


def process_all_pic():
    # pic_info_db.init_all()
    # face_info_db.delete_all()
    total_count = pic_info_db.get_pic_total_count()
    print(f"当前图片总数为{total_count}")
    unprocessed_count = pic_info_db.get_pic_un_detect_total_count()
    print(f"当前待检测图片总数为{unprocessed_count}")
    if os.path.exists(save_path):
        print(f"当前目录:{save_path}已存在，执行删除")
        shutil.rmtree(save_path)
    # 记录总共进度
    with tqdm(total=unprocessed_count,
              bar_format="处理百分比：{percentage:3.0f}%|{bar}|已处理{n_fmt}/总数{total_fmt}") as total_bar:
        flag = True
        while flag :
            pic_list = pic_info_db.get_to_process_file_list()
            if not pic_list:
                flag = False
            for pic_info_domain, file_info_domain in pic_list:
                detect_executor.submit(handle_file, pic_info_domain, file_info_domain, total_bar)


def handle_file(pic_info_domain: pic_info_db.PicInfo, file_info_domain: file_info_db.FileInfo, bar: tqdm):
    # 前置检查
    file_info_domain = check_before_detect(file_info_domain)
    # 处理
    detect_face_and_save(pic_info_domain, file_info_domain)
    bar.update(1)


# 人脸检测之前先判断md5是否存在，如果不存在则处理，然后重新查询
def check_before_detect(file_info: file_info_db.FileInfo):
    if file_info.file_md5 == 'tmp':
        print(f"当前文件{file_info.file_path}md5 不存在，开始计算")
        file_md5.calculate_md5(file_id=file_info.id, file_path=file_info.file_path)
        file_info = file_info_db.get_by_id(file_info.id)
    return file_info


# 检测人脸数据，并保存
def detect_face_and_save(pic_info_domain: pic_info_db.PicInfo, file_info_domain: file_info_db.FileInfo):
    face_base_path = os.path.join(save_path, file_info_domain.file_md5)
    try:
        face_list = face_detect_and_save(file_info_domain.file_path, face_base_path)
        if face_list:
            # 检测到人脸数据
            pic_info_domain.face_count = len(face_list)
            pic_info_domain.face_icon_path = os.path.abspath(face_base_path)
            pic_info_domain.status = pic_info_db.PicHandleStatus.WAIT_CON.value
            add_face_info(pic_info_domain.id, face_list)
        else:
            pic_info_domain.status = pic_info_db.PicHandleStatus.DONE.value
    except Exception as e:
        print(f"图片{file_info_domain.file_path}检测失败，异常原因:{e}")
        pic_info_domain.status = pic_info_db.PicHandleStatus.ERROR.value
    pic_info_db.update_face_detect_result(pic_info_domain)


def add_face_info(pic_id, face_list):
    for face_path in face_list:
        face_info_db.add_face_info(face_info=face_info_db.FaceInfo(
            pic_id=pic_id,
            face_path=os.path.abspath(face_path)
        ))


def face_detect_and_save(file_path, face_base_path):
    # print(f"开始检测{file_path}的人脸数据，保存地址为{face_base_path}")
    # 读取图片
    image = Image.open(file_path).convert("RGB")
    # 返回的boxes是包括人脸的框的坐标，points表示的是人脸的五个关键点的坐标,probs是人脸的执行度
    boxes, probs, points = mtcnn.detect(image, landmarks=True)
    face_list = []
    if boxes is not None:
        if not os.path.exists(face_base_path):
            os.makedirs(face_base_path)
        for i, (box, point) in enumerate(zip(boxes, points)):
            # print(f"处理第{i}个人脸数据")
            # 对获取到的每个人脸进行裁剪
            # print(f"开始裁剪")
            face = image.crop(box)
            face_save_path = os.path.join(face_base_path, f'{i}.png')
            face.save(face_save_path)
            face_list.append(face_save_path)
    return face_list


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
