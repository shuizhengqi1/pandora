from fastapi import APIRouter
from file import file_handle, file_md5

from db.db_tools import drop_table, init_db
from tool import log_tool

app = APIRouter()


@app.get("/file_scan")
async def run_file_scan():
    # drop_table()
    file_handle.get_file_list()


@app.get("/init_db")
def init():
    init_db()
    return "初始化成功"


@app.get("/file_md5")
def run_md5_cal():
    file_md5.cal_all_md5()
