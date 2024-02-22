from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session
from sqlalchemy import select
from domain import file_info

table_name = 'pic_info'


class PicInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    file_id = Column(INTEGER)
    face_count = Column(INTEGER, comment="人脸数量")
    face_icon_path = Column(String, comment="人脸小图存储的地址")
    status = Column(String, comment="人脸小图存储的地址", default="init")


def add_pic_info(pic_info: PicInfo):
    with get_session() as session:
        session.add(pic_info)
        session.flush()
        return pic_info.id


def get_pic_total_count():
    with get_session(False) as session:
        query = session.query(PicInfo)
        return query.count()


def get_pic_un_detect_total_count():
    with get_session(False) as session:
        query = session.query(PicInfo).filter(PicInfo.status == "init")
        return query.count()


def get_to_process_file_list():
    with get_session(False) as session:
        query = session.query(PicInfo, file_info.FileInfo).join(file_info.FileInfo,
                                                                PicInfo.file_id == file_info.FileInfo.id).filter(
            PicInfo.status == "init").limit(20)
        query.add_entity(PicInfo).add_entity(file_info.FileInfo)
        return query.all()


def update_face_detect_result(pic_info: PicInfo):
    with get_session() as session:
        update_pic_info = session.get(PicInfo, pic_info.id)
        update_pic_info.face_count = pic_info.face_count
        update_pic_info.face_icon_path = pic_info.face_icon_path
        update_pic_info.status = pic_info.status
