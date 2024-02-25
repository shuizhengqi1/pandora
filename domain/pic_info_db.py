from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session, engine, meta_data, Table
from sqlalchemy import select
from domain import file_info_db
from enum import Enum

table_name = 'pic_info'


class PicHandleStatus(Enum):
    INIT = "init"
    DONE = "done"
    WAIT_CON = "wait_con"
    ERROR = "error"


class PicInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    file_id = Column(INTEGER)
    face_count = Column(INTEGER, comment="人脸数量")
    face_icon_path = Column(String, comment="人脸小图存储的地址")
    status = Column(String, comment="人脸小图存储的地址", default="init")


def delete_all():
    with get_session() as session:
        session.delete()
        print(f"清理所有数据")


def init_all():
    with get_session() as session:
        pic_list = session.query(PicInfo).all()
        for pic in pic_list:
            pic.status = PicHandleStatus.INIT.value
            pic.face_count = 0
            pic.face_icon_path = ""
        print("清理所有照片的初始数据")


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
        query = session.query(PicInfo).filter(PicInfo.status == PicHandleStatus.INIT.value)
        return query.count()


def get_to_process_file_list():
    with get_session(False) as session:
        query = session.query(PicInfo, file_info_db.FileInfo).join(file_info_db.FileInfo,
                                                                   PicInfo.file_id == file_info_db.FileInfo.id).filter(
            PicInfo.status == "init").limit(20)
        query.add_entity(PicInfo).add_entity(file_info_db.FileInfo)
        return query.all()


def update_face_detect_result(pic_info: PicInfo):
    with get_session() as session:
        update_pic_info = session.get(PicInfo, pic_info.id)
        update_pic_info.face_count = pic_info.face_count
        update_pic_info.face_icon_path = pic_info.face_icon_path
        update_pic_info.status = pic_info.status
