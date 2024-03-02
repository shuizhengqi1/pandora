from fastapi import APIRouter
from file import file_handle, file_md5
from domain import base_config_db, media_type_db

from db.db_tools import drop_table, init_db
from tool import log_tool

app = APIRouter()


@app.get("/file_scan")
async def run_file_scan():
    file_handle.get_file_list()


@app.get("/init_db")
def init(drop: bool):
    if drop:
        drop_table()
    init_db()
    if drop:
        base_config_db.init()
        media_type_db.init()
    return "初始化成功"


@app.get("/file_md5")
def run_md5_cal():
    file_md5.cal_all_md5()
