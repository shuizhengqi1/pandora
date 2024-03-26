from web.frontend import ui


def menu() -> None:
    ui.link('文件处理', '/ui/file/list').classes(replace="text-white")
