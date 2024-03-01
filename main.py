import uvicorn
from fastapi import FastAPI
from web.config_api import app as config_api
from web.file_api import app as file_api
from db.db_tools import init_db
from domain import media_type_db, base_config_db

app = FastAPI()
app.include_router(config_api, prefix="/config")
app.include_router(file_api, prefix="/file")

if __name__ == '__main__':
    init_db()
    media_type_db.init()
    base_config_db.init()
    uvicorn.run(app="main:app")
