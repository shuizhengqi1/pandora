from fastapi import APIRouter
from picture import object_detect
from tool import executor_tool
from domain import file_info_db, pic_info_db

app = APIRouter()


@app.get("/detect")
async def run_face_detect(file_id: int):
    file_info = file_info_db.get_by_id(file_id)
    pic_info = pic_info_db.get_by_file_id(file_id)
    object_detect.start_detect(file_info, pic_info)
    return "物体检测完成"


@app.get("/detect")
async def run_face_detect_all():
    await object_detect.start_detect_all()
    return "物体检测开始"
