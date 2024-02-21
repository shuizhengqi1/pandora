from db.db_base import DbBase, Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB

table_name = 'pic_face_relation'


class PicFaceRelation(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    face_id = Column(INTEGER, primary_key=True)
    pic_id = Column(INTEGER, primary_key=True)

