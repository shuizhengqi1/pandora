from domain.face_info_db import FaceInfo
from domain.file_info_db import FileInfo
from domain.pic_info_db import PicInfo
from domain.video_info_db import VideoInfo
from domain.pic_face_relation_db import PicFaceRelation
from domain.base_config_db import BaseConfig
from domain.media_type_db import MediaType
from domain.object_detect_db import ObjectDetect
from db.db_base import get_session

domain_list = [FaceInfo, FileInfo, PicInfo, VideoInfo, PicFaceRelation, BaseConfig, MediaType, ObjectDetect]

clean_domain_list = [FaceInfo, FileInfo, PicInfo, VideoInfo, PicFaceRelation, ObjectDetect]


def clean_all():
    with get_session(True) as session:
        for domain in clean_domain_list:
            session.query(domain).delete()
            print(f"已清理{domain.__tablename__}数据")
