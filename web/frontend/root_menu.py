from web.frontend import ui


def menu() -> None:
    ui.link('文件列表', '/ui/file/list').classes(replace="text-white")
    ui.link('文件处理', '/ui/file/').classes(replace="text-white")
    ui.link('配置管理', '/ui/config/').classes(replace="text-white")
