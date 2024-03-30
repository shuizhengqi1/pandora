from nicegui import APIRouter, ui
from web.frontend import page_template
from web.api.file import file_view

router = APIRouter()


@router.page("/list", title="文件列表")
async def file_table():
    with page_template.frame("信息展示"):
        columns = [
            {'name': 'fileName', 'label': '文件名', 'field': 'fileName', 'required': True, 'align': 'left'},
            {'name': 'fileSize', 'label': '文件大小', 'field': 'fileSize', 'sortable': True},
            {'name': 'fileMd5', 'label': '文件MD5', 'field': 'fileMd5', 'sortable': True},
            {'name': 'filePath', 'label': '文件路径', 'field': 'filePath', 'align': 'left'},
            {'name': 'fileType', 'label': '文件类型', 'field': 'fileType'}
        ]
        file_page_info = await file_view.page_list(20, 1)
        file_list = [file_info.dict() for file_info in file_page_info.data]
        ui.table(columns=columns, rows=file_list, row_key="fileName")
        ui.pagination(file_page_info.pageNum, file_page_info.totalPageCount, direction_links=True)


@router.page("/", title="文件列表")
async def file_table():
    with page_template.frame("潘多拉"):
        ui.label("文件列表")
