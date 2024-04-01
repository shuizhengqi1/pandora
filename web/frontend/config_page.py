from nicegui import APIRouter, ui
from web.frontend import page_template
from web.api.file import file_view
from web.api import config_api

router = APIRouter()

config_map = None


@ui.refreshable
async def config_table() -> None:
    with ui.column():
        global config_map
        config_map = await config_api.show_config_info()
        # 扫描地址
        with ui.row():
            ui.label("扫描地址").style("width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map["start_dir"]).bind_value_to(config_map, "start_dir",
                                                                  lambda value: value).style("width: 300px")
            # 扫描地址
        with ui.row():
            ui.label("忽略的目录").style("width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map['skip_dir_name']).bind_value_to(config_map, "skip_dir_name",
                                                                      lambda value: value).style("width: 300px")
        with ui.row():
            ui.label("进度保存目录").style("width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map['scan_process_path']).bind_value_to(config_map, "scan_process_path",
                                                                          lambda value: value).style("width: 300px")


@router.page("/", title="配置读取")
async def config_page_index():
    with page_template.frame("配置查看"):
        with ui.row():
            await config_table()
        with ui.row():
            ui.button("保存", on_click=lambda: save_config(config_map))
            ui.button("刷新", on_click=lambda: config_table.refresh())


async def save_config(config_map):
    print(f"new value is {config_map}")
    await config_api.change_config(config_map)
    ui.notify(f"配置更新成功")


async def refresh_config_info():
    # 重新获取配置信息并更新config_map
    new_config_map = await config_api.show_config_info()
    # 更新字典，这里需要注意线程安全和数据同步的问题
    config_map.update(new_config_map)
