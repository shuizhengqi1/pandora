from fastapi import APIRouter
from web.api.file.file_md5_api import app as file_md5_router
from web.api.file.file_api import app as file_router
from web.api.file.file_scan_api import app as file_scan_router
from web.api.file.file_view_api import app as file_view_router

app = APIRouter(prefix="/api/file")
app.include_router(file_md5_router)
app.include_router(file_scan_router)
app.include_router(file_view_router)
app.include_router(file_router)
