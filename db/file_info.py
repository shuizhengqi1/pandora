from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, DATETIME, SMALLINT

Base = declarative_base()

class FileInfo(Base):
    __tablename__ = 'file_info'

    id = Column(INTEGER, primary_key=True)
    file_path = Column(String, comment="文件路径")
    file_md5 = Column(String, comment="文件md5，初始为空", default="tmp")
    file_name = Column(String, comment="文件名称")
    file_type = Column(String, comment="文件类型")
    file_size = Column(INTEGER, comment="文件大小，单位是MB")
    file_suffix = Column(INTEGER, comment="文件大小，单位是MB")
    create_time = Column(DATETIME, comment="创建时间")
    modify_time = Column(DATETIME, comment="更新时间")


class VideoInfo(Base):
    __tablename__ = 'video_info'
    id = Column(INTEGER, primary_key=True)
    file_id = Column(INTEGER)
    status = Column(SMALLINT, comment="处理状态")
    face_count = Column(INTEGER, comment="人脸数量")
    face_detect_path = Column(String, comment="人脸检测路径")
    audio_detect_path = Column(String, comment="音频检测路径")


class PicInfo(Base):
    __tablename__ = 'pic_info'
    id = Column(INTEGER, primary_key=True)
    pic_id = Column(INTEGER)
    face_count = Column(INTEGER, comment="人脸数量")

