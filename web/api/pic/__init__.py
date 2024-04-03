from fastapi import APIRouter
from web.api.pic.face_api import app as face_router
from web.api.pic.pic_operate_api import app as face_operate_router

app = APIRouter(prefix="/api/pic")
app.include_router(face_router, prefix="/face")
app.include_router(face_operate_router, prefix="/op")
