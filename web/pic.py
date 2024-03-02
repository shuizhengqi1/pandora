from typing import Union
from fastapi import APIRouter
from picture import face_detect

app = APIRouter()


@app.get("/face_detect")
async def run_face_detect():
    face_detect.process_all_pic()
    return "成功检测人脸"
