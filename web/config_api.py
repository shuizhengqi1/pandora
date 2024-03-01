from typing import Union
from fastapi import APIRouter
from domain import base_config_db

app = APIRouter()


@app.get("/change_dir")
def get_config_list(new_dir):
    base_config_db.change_config("start_dir", new_dir)
