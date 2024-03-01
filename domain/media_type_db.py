from db.db_base import Base, Column, INTEGER, String, LargeBinary, SMALLINT, BLOB, get_session
from enum import Enum
from data import config

table_name = "media_type"

media_type_list = ["video", "pic", "document"]
suffix_type_map = dict()


class MediaType(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    media_type = Column(String)
    media_suffix = Column(String)


def get_media_type_map(media_type):
    with get_session(False) as session:
        query = session.query(MediaType).filter(MediaType.media_type == media_type)
        return query.all()


def get_all():
    with get_session(False) as session:
        return session.query(MediaType).all()


def get_media_type_by_suffix(suffix):
    return suffix_type_map[suffix]


def init_local_suffix_map():
    global suffix_type_map
    result = get_all()
    if result:
        for item in result:
            suffix_type_map[item.media_suffix] = item.media_type


def check_and_init():
    with get_session(True) as session:
        for media_type in media_type_list:
            query = session.query(MediaType).filter(MediaType.media_type == media_type).all()
            if not query and config.config_json["type_map"][media_type]:
                for item in config.config_json["type_map"][media_type]:
                    session.add(MediaType(media_type=media_type, media_suffix=item))


def init():
    check_and_init()
    init_local_suffix_map()
    print("媒体文件加载完毕")
