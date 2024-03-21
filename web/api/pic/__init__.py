from fastapi import APIRouter
from web.api.pic.face_api import app as face_router

app = APIRouter(prefix="/api/pic")
app.include_router(face_router, prefix="/face")
