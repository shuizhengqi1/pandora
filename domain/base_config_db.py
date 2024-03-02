from db.db_base import Base, Column, INTEGER, String, LargeBinary, SMALLINT, BLOB, get_session
from enum import Enum
from data import config
import json

table_name = "base_config"

config_key_list = ["start_dir", "scan_interval", "scan_process_path", "skip_dir_name"]


class BaseConfig(Base):
    __tablename__ = table_name
    id = Column(INTEGER, primary_key=True)
    config_key = Column(String)
    config_value = Column(String)


def check_config_and_init(config_key):
    with get_session(True) as session:
        query = session.query(BaseConfig).filter(BaseConfig.config_key == config_key)
        result = query.first()
        print(f"{config_key}值为：{result}")
        if not result and config.config_json[config_key]:
            if isinstance(config.config_json[config_key], list):
                config_value = json.dumps(config.config_json[config_key])
            else:
                config_value = config.config_json[config_key]
            print(f"{config_key}不存在，初始化")
            baseConfig = BaseConfig(config_key=config_key, config_value=str(config_value))
            session.add(baseConfig)


def change_config(config_key, config_value):
    with get_session(True) as session:
        query = session.query(BaseConfig).filter(BaseConfig.config_key == config_key)
        if not query:
            baseConfig = BaseConfig(config_key=config_key, config_value=config_value)
            session.add(baseConfig)
        else:
            print(f"更新:{config_key}为{config_value}")
            query.first().config_value = config_value


def get_all_config():
    with get_session(False) as session:
        return session.query(BaseConfig).all()


def get_config(config_key):
    with get_session(True) as session:
        query = session.query(BaseConfig).filter(BaseConfig.config_key == config_key)
        result = query.first()
        if result:
            return result.config_value


def init():
    for key in config_key_list:
        check_config_and_init(key)
    print("配置文件加载完毕")
