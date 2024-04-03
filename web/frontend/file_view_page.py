from nicegui import APIRouter, ui, events
from web.frontend import page_template
from web.api.file import file_view_api, file_api, file_scan_api

router = APIRouter()

file_data_list = None
page_size = 20
current_page = 1

pagination = {}


@router.page("/list", title="文件列表")
async def show_file_table() -> None:
    with page_template.frame("信息展示"):
        await file_table()


@ui.refreshable
async def file_table() -> None:
    global current_page
    columns = [
        {'name': 'fileId', 'label': '文件id', 'field': 'fileId', 'required': True, 'align': 'left'},
        {'name': 'fileName', 'label': '文件名', 'field': 'fileName', 'required': True, 'align': 'left'},
        {'name': 'fileSize', 'label': '文件大小', 'field': 'fileSize', 'sortable': True},
        {'name': 'fileMd5', 'label': '文件MD5', 'field': 'fileMd5', 'sortable': True},
        {'name': 'filePath', 'label': '文件路径', 'field': 'filePath', 'align': 'left'},
        {'name': 'fileType', 'label': '文件类型', 'field': 'fileType'}
    ]

    file_page_info = await file_view_api.page_list(page_size, current_page)
    file_list = [file_info.dict() for file_info in file_page_info.data]
    ui.table(columns=columns,
             rows=file_list,
             pagination={'rowsPerPage': file_page_info.pageSize, 'page': current_page,
                         'rowsNumber': file_page_info.totalCount},
             on_pagination_change=on_pagination_change,
             row_key="fileName")


async def on_pagination_change(pagination):
    global pageInfo
    pageInfo['page'] = pagination['page']
    pageInfo['rowsPerPage'] = pagination['rowsPerPage']
    file_page_info = await file_view_api.page_list(pageInfo['page'], pageInfo['rowsPerPage'])
    file_table.refresh()


@router.page("/", title="文件列表")
async def file_page_index():
    with page_template.frame("潘多拉"):
        with ui.row():
            ui.button("扫描文件", on_click=clean_and_start_scan)
            ui.button("计算md5")
            ui.button("物体检测")


async def clean_and_start_scan():
    await file_scan_api.run_file_scan()
    ui.notify("已清理数据，并开始扫描")
