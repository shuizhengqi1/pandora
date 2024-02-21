from db.db_base import DbBase, Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB

table_name = 'video_info'


class VideoInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    file_id = Column(INTEGER)
    status = Column(SMALLINT, comment="处理状态")
    face_count = Column(INTEGER, comment="人脸数量")
    face_detect_path = Column(String, comment="人脸检测路径")
    audio_detect_path = Column(String, comment="音频检测路径")
