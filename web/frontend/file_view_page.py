from nicegui import APIRouter, ui, events
from web.frontend import page_template
from web.api.file import file_view_api, file_api, file_scan_api, file_md5_api
from web.api.pic import pic_operate_api
from tool import global_count

router = APIRouter()

file_data_list = None
pagination = {
    "page": 1,
    "rowsPerPage": 20,
    "descending": "s",
    "rowsNumber": 999
}


@router.page("/list", title="文件列表")
async def show_file_table() -> None:
    with page_template.frame("信息展示"):
        await file_table()


@ui.refreshable
async def file_table() -> None:
    columns = [
        {'name': 'fileId', 'label': '文件id', 'field': 'fileId', 'required': True, 'align': 'left'},
        {'name': 'fileName', 'label': '文件名', 'field': 'fileName', 'required': True, 'align': 'left'},
        {'name': 'fileSize', 'label': '文件大小', 'field': 'fileSize', 'sortable': True},
        {'name': 'fileMd5', 'label': '文件MD5', 'field': 'fileMd5', 'sortable': True},
        {'name': 'filePath', 'label': '文件路径', 'field': 'filePath', 'align': 'left'},
        {'name': 'fileType', 'label': '文件类型', 'field': 'fileType'}
    ]

    table = ui.table(columns=columns,
                     rows=await load_file_info(),
                     selection="multiple",
                     pagination=pagination,
                     row_key="fileName")
    table.add_slot("top", """
         <q-select
          v-model="visibleColumns"
          outlined
          dense
          options-dense
          :display-value="$q.lang.table.columns"
          emit-value
          map-options
          :options="pic"
          option-value="name"
          options-cover
          style="min-width: 150px"
        />
    """)
    table.on("request", on_file_page_change)


async def load_file_info():
    global pagination
    file_page_info = await file_view_api.page_list(pagination['rowsPerPage'], pagination['page'])
    pagination['page'] = file_page_info.pageNum
    pagination['rowsPerPage'] = file_page_info.pageSize
    pagination['rowsNumber'] = file_page_info.totalCount
    return [file_info.dict() for file_info in file_page_info.data]


async def on_file_page_change(request):
    global pagination
    pagination.update(request.args['pagination'])
    file_table.refresh()


@router.page("/", title="文件列表")
async def file_page_index():
    with (page_template.frame("潘多拉")):
        with ui.row():
            ui.button("扫描文件", on_click=clean_and_start_scan).bind_enabled_from(not global_count.scan_flag)
            ui.button("停止扫描", on_click=clean_and_start_scan
                      ).bind_visibility_from(
                global_count.scan_flag).bind_enabled_from(global_count.scan_flag)
            ui.button("计算md5", on_click=cal_md5).bind_enabled_from(global_count.md5_flag)
            ui.button("停止计算md5", on_click=global_count.stop_file_md5()).bind_enabled_from(
                not global_count.md5_flag).bind_visibility_from(
                not global_count.md5_flag)
            ui.button("物体检测", on_click=object_detect)


async def cal_md5():
    await file_md5_api.run_md5_cal()
    ui.notify("开始计算md5")


async def object_detect():
    await pic_operate_api.run_face_detect_all()
    ui.notify("开始物体检测")


async def clean_and_start_scan():
    await file_scan_api.run_file_scan()
    ui.notify("已清理数据，并开始扫描")
