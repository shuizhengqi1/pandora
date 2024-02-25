from db.db_base import Base, Column, INTEGER, String, LargeBinary, SMALLINT, BLOB, get_session

table_name = "face_info"


class FaceInfo(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    face_feature = Column(LargeBinary, comment="人脸向量数据")
    face_path = Column(String, comment="人脸存储路径")
    pic_id = Column(INTEGER)


def delete_all():
    with get_session() as session:
        session.query(FaceInfo).delete()
        print(f"清理所有数据")


def add_face_info(face_info: FaceInfo):
    with get_session() as session:
        session.add(face_info)
        session.flush()
        return face_info.id
