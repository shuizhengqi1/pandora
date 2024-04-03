from fastapi import APIRouter
from picture import object_detect
from tool import executor_tool
from domain import file_info_db

app = APIRouter()


@app.get("/detect")
async def run_face_detect(file_id: int):
    file_info = file_info_db.get_by_id(file_id)
    object_detect.start_detect(file_info)
    return "物体检测完成"
