from db.db_base import Base, Column, INTEGER, String, LargeBinary, SMALLINT, BLOB, get_session
from data import config
from domain.enums import MediaTypeEnum

table_name = "media_type"


class MediaType(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    media_type = Column(String)
    media_suffix = Column(String)


def get_media_type_map(media_type):
    with get_session(False) as session:
        query = session.query(MediaType).filter(MediaType.media_type == media_type)
        return query.all()


def get_all_suffix():
    with get_session(False) as session:
        result = session.query(MediaType).all()
        if result:
            return [media_type.media_suffix for media_type in result]


def get_all():
    with get_session(False) as session:
        return session.query(MediaType).all()


def get_media_type_by_suffix(suffix):
    return suffix_type_map[suffix.lower()]


def init_local_suffix_map():
    result = get_all()
    local_data = {}
    if result:
        for item in result:
            local_data[item.media_suffix] = item.media_type
    return local_data


def check_and_init():
    with get_session(True) as session:
        for media_type in MediaTypeEnum:
            query = session.query(MediaType).filter(MediaType.media_type == media_type.value).all()
            if not query and config.config_json["type_map"][media_type.value]:
                for item in config.config_json["type_map"][media_type.value]:
                    session.add(MediaType(media_type=media_type.value, media_suffix=item))


suffix_type_map = init_local_suffix_map()


def init():
    check_and_init()
    print("媒体文件加载完毕")
