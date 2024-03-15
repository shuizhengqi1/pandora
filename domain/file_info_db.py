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


def query_unprocessed_file_list():
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_md5 == 'tmp').limit(20)
        result_list = query.all()
        return result_list


def get_all_data():
    with get_session(False) as session:
        query = session.query(FileInfo)
        result_list = query.all()
        return result_list


def page_list(file_type, page_size, page_num):
    with get_session(False) as session:
        query = session.query(FileInfo)
        if file_type:
            query = query.filter(FileInfo.file_type == file_type)
        query = query.limit(page_size).offset((page_num - 1) * page_size)
        result_list = query.all()
        return result_list


def query_need_cal_md5_count():
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_md5 == 'tmp')
        return query.count()


def get_file_total_count():
    with get_session(False) as session:
        query = session.query(FileInfo)
        return query.count()


def get_file_by_md5(md5):
    if not md5:
        raise ValueError("要查询的md5不能为空")
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_md5 == md5)
        return query.all()


def get_type_count():
    with get_session(False) as session:
        query = session.query(FileInfo.file_type, func.count(FileInfo.file_type)).group_by(FileInfo.file_type)
        return query.all()


def get_by_id(file_id):
    with get_session(False) as session:
        return session.get(FileInfo, file_id)


def update_file_md5(_id, md5):
    with get_session(True) as session:
        file_info = session.get(FileInfo, _id)
        file_info.file_md5 = md5


def get_by_id_list(file_id_list):
    with get_session(False) as session:
        return session.query(FileInfo).filter(FileInfo.id.in_(file_id_list)).all()


def delete_by_id_list(file_id_list):
    with get_session(False) as session:
        return session.query(FileInfo).filter(FileInfo.id.in_(file_id_list)).delete()


def find_duplicate_file_list():
    with (get_session() as session):
        # 查询重复的md5数据
        duplicate_md5_subquery = session.query(
            FileInfo.file_md5,
            func.count(FileInfo.file_md5).label('count'),
            func.min(FileInfo.id).label('min_id')  # 获取每组文件中ID最小的文件
        ).group_by(
            FileInfo.file_md5
        ).having(
            func.count(FileInfo.file_md5) > 1
        ).subquery()

        # 关联原始FileInfo表和子查询，以获取每组的第一个文件的详细信息
        total_query = session.query(
            FileInfo,
            duplicate_md5_subquery.c.count
        ).join(
            duplicate_md5_subquery,
            FileInfo.file_md5 == duplicate_md5_subquery.c.file_md5
        ).filter(
            FileInfo.id == duplicate_md5_subquery.c.min_id  # 只选择每组中ID最小的文件
        ).order_by(
            duplicate_md5_subquery.c.count.desc()
        )
        duplicate_file_list = total_query.all()
        if duplicate_file_list:
            for file_info, count in duplicate_file_list:
                print(
                    f"文件名:{file_info.file_name} 文件路径:{file_info.file_path} 文件md5:{file_info.file_md5} 重复个数:{count}")
