import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI
from web.config_api import app as config_api
from web.file_api import app as file_api
from web.pic import app as pic_api
from db.db_tools import init_db
from domain import media_type_db, base_config_db
from tool import executor_tool

app = FastAPI()
app.include_router(config_api, prefix="/config")
app.include_router(file_api, prefix="/file")
app.include_router(pic_api, prefix="/pic")


@app.get("/")
async def root():
    return "root"


if __name__ == '__main__':
    init_db()
    media_type_db.init()
    base_config_db.init()
    uvicorn.run("main:app", host="0.0.0.0", access_log=True, reload=True)
    sys.exit()
