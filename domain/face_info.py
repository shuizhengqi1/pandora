from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session


class FaceInfo(Base):
    __tablename__ = "face_info"
    id = Column(INTEGER, primary_key=True)
    face_feature = Column(BLOB, comment="人脸向量数据")
    face_path = Column(String, comment="人脸存储路径")
    pic_id = Column(INTEGER, primary_key=True)


def add_face_info(face_info: FaceInfo):
    with get_session() as session:
        session.add(face_info)
        session.flush()
        return face_info.id
