from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session
from db.db_tools import *

table_name = 'file_info'


class FileInfo(Base):
    __tablename__ = table_name

    id = Column(INTEGER, primary_key=True)
    file_path = Column(String, comment="文件路径")
    file_md5 = Column(String, comment="文件md5，初始为空", default="tmp")
    file_name = Column(String, comment="文件名称")
    file_type = Column(String, comment="文件类型")
    file_size = Column(INTEGER, comment="文件大小，单位是MB")
    file_suffix = Column(INTEGER, comment="文件大小，单位是MB")
    create_time = Column(DATETIME, comment="创建时间")
    modify_time = Column(DATETIME, comment="更新时间")


def add_file_info(file_info: FileInfo):
    with get_session() as session:
        session.add(file_info)


def query_unprocessed_file_list(file_type):
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_type == file_type).filter(
            FileInfo.file_md5 == 'tmp').limit(20)
        result_list = query.all()
        return result_list


def query_total_count(file_type):
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_type == file_type).filter(
            FileInfo.file_md5 == 'tmp')
        return query.count()


def update_file_md5(_id, md5):
    with get_session() as session:
        file_info = session.get(FileInfo, _id)
        file_info.file_md5 = md5
