from picture.abs_face_handle import AbcFaceHandle
from facenet_pytorch import MTCNN, InceptionResnetV1
import os

from PIL import Image
import torch


class Pytorch(AbcFaceHandle):
    device = torch.device('cuda')
    mtcnn = MTCNN(device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval().cuda(device)

    def face_detect(self, file_path: str, face_base_path: str):
        # print(f"开始检测{file_path}的人脸数据，保存地址为{face_base_path}")
        # 读取图片
        image = Image.open(file_path).convert("RGB")
        # 返回的boxes是包括人脸的框的坐标，points表示的是人脸的五个关键点的坐标,probs是人脸的执行度
        boxes, probs, points = self.mtcnn.detect(image, landmarks=True)
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

    def face_recon(self, face_path):
        try:
            image = Image.open(face_path)
        except Exception as e:
            print(f"{face_path}文件不存在")
            return
        embedding = self.resnet(image.unsqueeze(0)).detach().numpy()[0]
        return embedding
