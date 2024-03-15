from db.db_tools import drop_table, init_db
from tool import executor_tool
from fastapi import APIRouter
from file import file_handle, file_md5
from pydantic import BaseModel

app = APIRouter()


class FileCount(BaseModel):
    totalCount: int
    needCalMd5Count: int


@app.get("/run_cal")
async def run_md5_cal():
    executor_tool.api_pool.submit(file_md5.cal_all_md5)
    return "成功开始计算"


@app.get("/total_count")
async def get_total_count_info():
    file_count, need_cal_md5_count = file_md5.get_count_info()
    return FileCount(totalCount=file_count, needCalMd5Count=need_cal_md5_count)
