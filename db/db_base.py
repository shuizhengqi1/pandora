from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from tool import log_tool

# noinspection PyUnresolvedReferences
from sqlalchemy import create_engine, MetaData, Table, inspect, Column, INTEGER, String, DATETIME, SMALLINT, BLOB, \
    LargeBinary

# Base信息
Base = declarative_base()

engine = create_engine("sqlite:///./data/pandora.db")

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
