from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData, Table, inspect
from db.db_base import Base, engine, inspector, refresh
from domain import domain_list
from tool import log_tool


@log_tool.log_process("初始化db")
def init_db():
    for table in domain_list:
        if not inspector.has_table(table.__tablename__):
            print(f"初始化db")
            Base.metadata.create_all(engine, checkfirst=True)
            refresh()
            break
    refresh()


@log_tool.log_process("drop表")
def drop_table():
    metaData = MetaData()
    for table in domain_list:
        table_info = Table(table.__tablename__, metaData)
        if inspector.has_table(table.__tablename__):
            print(f"当前表:{table.__tablename__}已经存在了，执行drop")
            table_info.drop(engine)
            print(f"{table.__tablename__}表drop完成")
