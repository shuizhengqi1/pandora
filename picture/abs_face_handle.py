from abc import ABC, abstractmethod


class AbcFaceHandle(ABC):

    # 面部识别，检测是否包含人脸数据
    @abstractmethod
    def face_detect(self, file_path: str, face_base_path: str):
        pass

    # 根据检测出来的人脸数据，识别具体的人脸特征向量
    @abstractmethod
    def face_recon(self, face_path):
        pass
