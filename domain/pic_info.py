from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB

table_name = 'pic_info'


class PicInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    pic_id = Column(INTEGER)
    face_count = Column(INTEGER, comment="人脸数量")
