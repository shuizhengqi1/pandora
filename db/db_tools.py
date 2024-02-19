from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData, Table, inspect
from db.file_info import FileInfo, Base

engine = create_engine("sqlite:///./data/pandora.db")
inspector = inspect(engine)

Session = sessionmaker(bind=engine)


@contextmanager
def get_session(auto_commit=True):
    session = Session()
    try:
        yield session
        if auto_commit:
            session.commit()
    except Exception as e:
        print(f"出现了异常 :{e}")
        raise e
    finally:
        session.close()


def add_file_info(file_info: FileInfo):
    with get_session() as session:
        session.add(file_info)


def query_unprocessed_list(file_type):
    with get_session(False) as session:
        query = session.query(FileInfo).filter(FileInfo.file_type == file_type).filter(FileInfo.file_md5 == 'tmp').limit(20)
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


def init_db():
    file_info_exist, video_info_exist, pic_info_exist = check_table_exist()
    if not file_info_exist or video_info_exist or pic_info_exist:
        Base.metadata.create_all(engine)


def check_table_exist():
    return inspector.has_table('file_info'), inspector.has_table('video_info'), inspector.has_table('pic_info')


def drop_table():
    metaData = MetaData()
    file_info = Table('file_info', metaData)
    video_info = Table('video_info', metaData)
    pic_info = Table('pic_info', metaData)
    file_info_exist, video_info_exist, pic_info_exist = check_table_exist()
    if file_info_exist:
        file_info.drop(engine)
    if video_info_exist:
        video_info.drop(engine)
    if pic_info_exist:
        pic_info.drop(engine)
