from db.db_base import DbBase, Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB


class FaceInfo(Base):
    __tablename__ = "face_info"
    id = Column(INTEGER, primary_key=True)
    face_feature = Column(BLOB, comment="人脸向量数据")
    face_path = Column(String, comment="人脸存储路径")
