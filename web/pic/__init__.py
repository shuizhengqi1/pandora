from fastapi import APIRouter
from web.pic.face_api import app as face_router

app = APIRouter()
app.include_router(face_router, prefix="/face")


