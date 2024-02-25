from sqlalchemy import func, select

from db.db_base import Base, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, get_session

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


def delete_all():
    with get_session() as session:
        session.delete()
        print(f"清理所有数据")


def add_file_info(file_info: FileInfo):
    with get_session() as session:
        session.add(file_info)
        session.flush()
        return file_info.id


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


def get_by_id(file_id):
    with get_session() as session:
        return session.get(FileInfo, file_id)


def update_file_md5(_id, md5):
    with get_session() as session:
        file_info = session.get(FileInfo, _id)
        file_info.file_md5 = md5


def find_duplicate_file_list():
    with (get_session() as session):
        # 查询重复的md5数据
        duplicate_md5_query = select(FileInfo.file_md5, func.count(FileInfo.file_md5)).group_by(
            FileInfo.file_md5).having(func.count(FileInfo.file_md5) > 1).alias()
        total_query = session.query(FileInfo, duplicate_md5_query.c.count).join(duplicate_md5_query,
                                                                                FileInfo.file_md5 ==
                                                                                duplicate_md5_query.c.file_md5
                                                                                ).order_by(FileInfo.file_md5)
        duplicate_file_list = total_query.all()
        if duplicate_file_list:
            for file_info, count in duplicate_file_list:
                print(
                    f"文件名:{file_info.file_name} 文件路径:{file_info.file_path} 文件md5:{file_info.file_md5} 重复个数:{count}")
