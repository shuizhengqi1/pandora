import sys
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from web.api.config_api import app as config_api
from web.api.file import app as file_api
from web.api.pic import app as pic_api
from db.db_tools import init_db
from domain import media_type_db, base_config_db
import atexit
from tool import executor_tool
import web.frontend
import webbrowser


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     webbrowser.open("http://localhost:8000/ui")
#     yield
#     # Clean up the ML models and release the resources


app = FastAPI(docs_url="/doc", redoc_url=None)
app.include_router(config_api)
app.include_router(file_api)
app.include_router(pic_api)

@app.get("/")
async def root():
    return "root"


web.frontend.init(app)

if __name__ == '__main__':
    init_db()
    media_type_db.init()
    base_config_db.init()
    atexit.register(executor_tool.clean)

    uvicorn.run("main:app", host="0.0.0.0", access_log=True, reload=True)
    sys.exit()
