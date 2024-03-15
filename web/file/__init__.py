from fastapi import APIRouter
from web.file.file_md5_api import app as file_md5_router
from web.file.file_api import app as file_router
from web.file.file_scan_api import app as file_scan_router
from web.file.file_view import app as file_view_router

app = APIRouter()
app.include_router(file_md5_router, prefix="/fileMd5")
app.include_router(file_scan_router, prefix="/fileScan")
app.include_router(file_view_router, prefix="/view")
app.include_router(file_router, prefix="")


