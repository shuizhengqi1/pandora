from db.db_base import Base, Column, INTEGER, String, LargeBinary, SMALLINT, BLOB, get_session
from enum import Enum
from domain.enums import FaceReconStatus

table_name = "face_info"


class FaceInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    face_feature = Column(LargeBinary, comment="人脸向量数据")
    face_path = Column(String, comment="人脸存储路径")
    pic_id = Column(INTEGER)
    status = Column(INTEGER, comment="人脸识别状态")


def delete_all():
    with get_session() as session:
        session.query(FaceInfo).delete()
        print(f"清理所有数据")


def get_face_total_count():
    with get_session(False) as session:
        query = session.query(FaceInfo)
        return query.count()


def get_to_process_face_list(page_size, page_number):
    with get_session(False) as session:
        query = session.query(FaceInfo).filter(
            FaceInfo.status == FaceReconStatus.INIT.value).offset((page_number - 1) * page_size).limit(page_size)
        return query.all()


def get_face_need_process_count():
    with get_session() as session:
        query = session.query(FaceInfo).filter(FaceInfo.status == FaceReconStatus.INIT.value)
        return query.count()


def add_face_info(face_info: FaceInfo):
    with get_session() as session:
        session.add(face_info)
        session.flush()
        return face_info.id


def update_face_info(face_info: FaceInfo):
    with get_session(True) as session:
        update_data = session.get(FaceInfo, face_info.id)
        if face_info.face_feature:
            update_data.face_feature = face_info.face_feature
        update_data.status = face_info.status
