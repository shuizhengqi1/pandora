from nicegui import APIRouter, ui
from web.frontend import page_template
from web.api.file import file_view
from web.api import config_api

router = APIRouter()


@router.page("/", title="配置读取")
async def config_table():
    with page_template.frame("配置查看"):
        with ui.column():
            config_list = await config_api.show_config_info()
            for config in config_list:
                with ui.row():
                    # 使用 ui.label 创建标签
                    label = ui.label(config['fieldKey']).style("width: 200px;display: "
                                                               "flex;align-items: center;vertical-align: middle")
                    # 设置标签的宽度，避免过长
                    # 使用 ui.input 创建输入框
                    input_box = ui.input(value=config['fieldValue']).style("width: 300px")
                    # 设置输入框的宽度，使其不超过屏幕宽度
            with ui.row():
                submit_button = ui.button("保存")
                refresh_button = ui.button("刷新")
