from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session

table_name = 'pic_face_relation'


class PicFaceRelation(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    face_id = Column(INTEGER)
    pic_id = Column(INTEGER)


def delete_all():
    with get_session(True) as session:
        session.query(PicFaceRelation).delete()
        print(f"清理所有数据")
