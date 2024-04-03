from nicegui import APIRouter, ui
from domain.enums import ConfigKeyEnum
from web.frontend import page_template
from web.api.file import file_view_api
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
            ui.input(value=config_map[ConfigKeyEnum.START_DIR.value]).bind_value_to(config_map,
                                                                                    ConfigKeyEnum.START_DIR.value,
                                                                                    lambda value: value).style(
                "width: 300px")
            # 扫描地址
        with ui.row():
            ui.label("忽略的目录").style("width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map[ConfigKeyEnum.SKIP_DIR_NAME.value]).bind_value_to(config_map,
                                                                                        ConfigKeyEnum.SKIP_DIR_NAME.value,
                                                                                        lambda value: value).style(
                "width: 300px")
        with ui.row():
            ui.label("进度保存目录").style("width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map[ConfigKeyEnum.SCAN_PROCESS_PATH.value]).bind_value_to(config_map,
                                                                                            ConfigKeyEnum.SCAN_PROCESS_PATH.value,
                                                                                            lambda value: value).style(
                "width: 300px")

        with ui.row():
            ui.label("检测裁剪图保存地址").style(
                "width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map[ConfigKeyEnum.PIC_TMP_PATH.value]).bind_value_to(config_map,
                                                                                       ConfigKeyEnum.PIC_TMP_PATH.value,
                                                                                       lambda value: value).style(
                "width: 300px")

        with ui.row():
            ui.label("模型地址").style(
                "width: 200px;display: flex;align-items: center;vertical-align: middle")
            ui.input(value=config_map[ConfigKeyEnum.MODEL_PATH.value]).bind_value_to(config_map,
                                                                                     ConfigKeyEnum.MODEL_PATH.value,
                                                                                     lambda value: value).style(
                "width: 300px")


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
