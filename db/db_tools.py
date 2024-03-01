from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData, Table, inspect
from db.db_base import Base, engine
from domain import domain_list
from tool import log_tool


@log_tool.log_process("初始化db")
def init_db():
    inspector = inspect(engine)
    for table in domain_list:
        if not inspector.has_table(table.__tablename__):
            print(f"初始化db")
            Base.metadata.create_all(engine, checkfirst=True)
            break


def init_db_with_name(table_name):
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        print(f"初始化db")
        Base.metadata.create_all(engine, checkfirst=True)


@log_tool.log_process("drop表")
def drop_table():
    inspector = inspect(engine)
    for table in domain_list:
        if inspector.has_table(table.__tablename__):
            print(f"当前表:{table.__tablename__}已经存在了，执行drop")
            Base.metadata.tables[table.__tablename__].drop(engine)
            print(f"{table.__tablename__}表drop完成")
