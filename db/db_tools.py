from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData, Table, inspect
from db_base import Base, engine, inspector
from domain import domain_list


def init_db():
    for table in domain_list:
        if not inspector.has_table(table.__tablename__):
            Base.metadata.create_all(engine)
            break


def drop_table():
    metaData = MetaData()
    for table in domain_list:
        table_info = Table(table.__tablename__, metaData)
        if inspector.has_table(table.__tablename__):
            table_info.drop(engine)
