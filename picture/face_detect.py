from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np
import os

device = torch.device('cpu')
save_path = './test'
mtcnn = MTCNN(device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

os.makedirs(save_path, exist_ok=True)


def detect_face_and_save(path):
    image = Image.open(path)
    # 返回的boxes是包括人脸的框的坐标，points表示的是人脸的五个关键点的坐标,probs是人脸的执行度
    boxes, probs, points = mtcnn.detect(image, landmarks=True)
    print(f"检测到:{len(boxes)}个人脸")
    if boxes is not None:
        for i, (box, point) in enumerate(zip(boxes, points)):
            # 对获取到的每个人脸进行裁剪
            face = image.crop(box)
            mtcnn(face)
            face_embedding = resnet(mtcnn(face).unsqueeze(0)).detach().numpy()
            face_save_path = os.path.join(save_path, f'face_{i}.png')
            face.save(face_save_path)
            face_embedding_path = os.path.join(save_path, f'face_{i}_embedding.npy')
            np.save(face_embedding_path,face_embedding)


# def check1_embedding(face1,face2):
#     face1_embedding = resnet(mtcnn(face1).unsqueeze(0))
#     face2_embedding = resnet(mtcnn(face2).unsqueeze(0))
#     distance = (face1_embedding - face2_embedding).norm().item()
#     # 设定阈值并判断是否为同一个人
#     threshold = 1.0  # 阈值可以根据实际情况调整
#     if distance < threshold:
#         print("face1和face2是同一个人")
#     else:
#         print("face1和face2不是同一个人")


detect_face_and_save('/Users/yanghengxing/Pictures/WechatIMG205.jpg')

# 人脸检测
# 人脸识别
# 人脸特征保存
# 人脸特征对比
# 模型加载
