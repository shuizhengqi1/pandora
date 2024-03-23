from fastapi import FastAPI
from nicegui import ui
import web.frontend.page_template
import web.frontend.file_view_page


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
    def show() -> None:
        with page_template.frame("潘多拉"):
            ui.label('Hello, FastAPI!')
            # NOTE dark mode will be persistent for each user across tabs and server restarts
            ui.dark_mode()
            ui.checkbox('dark mode')

    fastapi_app.include_router(file_view_page.router, prefix="/ui/file")

    ui.run_with(
        fastapi_app,
        mount_path='/ui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',
        # NOTE setting a secret is optional but allows for persistent storage per user
    )
