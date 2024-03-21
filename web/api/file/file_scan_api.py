from fastapi import APIRouter

from file import file_handle
from tool import executor_tool

app = APIRouter(prefix="/fileScan")


@app.get("/start")
async def run_file_scan():
    executor_tool.api_pool.submit(file_handle.get_file_list)
    return "成功开始计算"
