from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session, engine, meta_data, Table, \
    FLOAT
from sqlalchemy import select
from domain import file_info_db
from enum import Enum

table_name = 'yolo'


class ObjectDetect(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    file_id = Column(INTEGER)
    object_name = Column(String, comment="监测到的物体名称")
    conf = Column(FLOAT, comment="置信度")
    object_crop_path = Column(String, comment="图片检测的地址")


def delete_by_file(file_id: int):
    with get_session(True) as session:
        session.query(ObjectDetect).filter(ObjectDetect.file_id == file_id).all().delete()


def add_object_detect(object_detect: ObjectDetect):
    object_detect.id = None
    with get_session() as session:
        session.add(object_detect)
        session.flush()
        return object_detect.id
