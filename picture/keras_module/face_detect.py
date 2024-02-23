import os.path
from keras_facenet import FaceNet
import cv2

from picture.abs_face_handle import AbcFaceHandle
from mtcnn import MTCNN


class Keras(AbcFaceHandle):
    mtcnn = MTCNN()
    facenet = FaceNet()

    def face_detect(self, file_path: str, face_base_path: str):
        print(f"开始检测{file_path}的人脸数据，保存地址为{face_base_path}")
        print(f"加载图片")
        originImage = cv2.imread(file_path)
        # print(f"设置色彩")
        # image = cv2.cvtColor(originImage, cv2.COLOR_BGR2RGB)
        print(f"检测")
        faces = self.mtcnn.detect_faces(originImage)
        print(f"共计检测到{len(faces)}个人脸数据")
        face_path_list = []
        if faces is not None:
            if not os.path.exists(face_base_path):
                print(f"当前目录不存在")
                os.makedirs(face_base_path, exist_ok=True)
            for i, face in enumerate(faces):
                x, y, w, h = face['box']
                face_img = originImage[y:y + h, x:x + w]
                face_path = os.path.join(face_base_path, f"{i}.jpg")
                cv2.imwrite(face_path, face_img)
                face_path_list.append(face_path)
        return face_path_list

    def face_recon(self, face_path):
        face_image = cv2.imread(face_path)
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face_embeddings = self.facenet.embeddings(face_image)

