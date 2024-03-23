from nicegui import APIRouter, app
from nicegui import ui
from web.frontend import page_template

router = APIRouter()


@router.page("/list", title="sad")
def file_table():
    columns = [
        {'name': 'fileName', 'label': '文件名', 'field': 'fileName', 'required': True, 'align': 'left'},
        {'name': 'fileSize', 'label': '文件大小', 'field': 'fileSize', 'sortable': True},
        {'name': 'fileMd5', 'label': '文件MD5', 'field': 'fileMd5', 'sortable': True},
        {'name': 'filePath', 'label': '文件路径', 'field': 'filePath', 'align': 'left'},
        {'name': 'fileType', 'label': '文件类型', 'field': 'fileType'}
    ]
    ui.table(columns=columns, rows=[], row_key="fileName")
    print("s")


@router.page("/", title="文件列表")
def file_table():
    ui.label("文件列表")
