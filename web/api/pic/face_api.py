from typing import Union
from fastapi import APIRouter
from picture import face_detect
from tool import executor_tool

app = APIRouter()


@app.get("/faceDetect")
async def run_face_detect():
    executor_tool.file_pool.submit(face_detect.process_all_pic)
    return "成功检测人脸"
