from fastapi import APIRouter
from domain import base_config_db

app = APIRouter(prefix="/api/config")


@app.get("/change_dir")
async def change_start_dir(new_dir: str):
    base_config_db.change_config("start_dir", new_dir.replace("\\", "\\\\"))


@app.get("/show")
async def show_config_info():
    result = base_config_db.get_all_config()
    config_map = {config.config_key: config.config_value for config in result}
    return config_map


@app.get("/change_config")
async def change_config(config_map: dict):
    for key, value in config_map.items():
        base_config_db.change_config(key, value)
