import asyncio
import atexit
from fastapi import APIRouter
from file import file_handle, file_md5
from domain import base_config_db, media_type_db
from pydantic import BaseModel
from db.db_tools import drop_table, init_db
from tool import executor_tool

app = APIRouter()


class FileCount(BaseModel):
    total_count: int
    need_cal_md5_count: int


@app.get("/file_scan")
async def run_file_scan():
    executor_tool.api_pool.submit(file_handle.get_file_list)
    return "成功开始计算"


@app.get("/init_db")
async def init(drop: bool):
    if drop:
        drop_table()
    init_db()
    if drop:
        base_config_db.init()
        media_type_db.init()
    return "初始化成功"


@app.get("/file_md5/run_cal")
async def run_md5_cal():
    executor_tool.api_pool.submit(file_md5.cal_all_md5)
    return "成功开始计算"


@app.get("/file_md5/total_count")
async def get_total_count_info():
    file_count, need_cal_md5_count = file_md5.get_count_info()
    return FileCount(total_count=file_count, need_cal_md5_count=need_cal_md5_count)
