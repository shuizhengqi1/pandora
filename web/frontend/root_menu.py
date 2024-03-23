from web.frontend import ui


def menu() -> None:
    ui.link('文件处理', '/file/').classes(replace="text-white")
