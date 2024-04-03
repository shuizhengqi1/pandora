from fastapi import APIRouter
from domain import base_config_db, media_type_db, file_info_db, pic_info_db, pic_face_relation_db, object_detect_db, \
    video_info_db
from db.db_tools import drop_table, init_db
from file import file_handle
from typing import List
from pydantic import BaseModel
import domain

app = APIRouter(prefix="")


class FileIdList(BaseModel):
    fileIdList: List[int]


@app.get("/init_db")
async def init(drop: bool):
    if drop:
        drop_table()
    init_db()
    if drop:
        base_config_db.init()
        media_type_db.init()
    return "初始化成功"


@app.post("/delete")
async def delete_file_list(file_id_list: FileIdList):
    file_list = file_info_db.get_by_id_list(file_id_list.fileIdList)
    if file_list:
        for file in file_list:
            file_handle.file_delete(file)


@app.post("/clean_data")
async def clean_all():
    domain.clean_all()
