from typing import Union
from fastapi import APIRouter
from domain import base_config_db

app = APIRouter()


@app.get("/change_dir")
def change_start_dir(new_dir: str):
    base_config_db.change_config("start_dir", new_dir.replace("\\", "\\\\"))


@app.get("/show")
def show_config_info():
    result = base_config_db.get_all_config()
    return [{"配置名": config.config_key, "配置值": config.config_value} for config in result]
