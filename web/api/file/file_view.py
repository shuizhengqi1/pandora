from fastapi import APIRouter
from domain import file_info_db, FileInfo
from pydantic import BaseModel
from web.api.vo.page_info import PageInfo

app = APIRouter(prefix="/view")


class TypeCountVo(BaseModel):
    typeName: str
    typeCount: int


class FileCountVo(BaseModel):
    fileTotalCount: int
    countList: list[TypeCountVo]


class FileInfoVo(BaseModel):
    fileName: str
    fileSize: str
    fileMd5: str
    filePath: str
    fileType: str

    def __init__(self, file_info: FileInfo):
        super().__init__(
            fileName=file_info.file_name,
            fileSize=f"{file_info.file_size}mb",
            fileMd5=file_info.file_md5,
            filePath=file_info.file_path,
            fileType=file_info.file_type
        )

@app.get("/getCount")
async def get_count():
    total_count = file_info_db.get_file_total_count()
    types_count = file_info_db.get_type_count()
    return FileCountVo(fileTotalCount=total_count,
                       countList=[TypeCountVo(typeName=_type[0], typeCount=_type[1]) for _type in types_count])


@app.get("/list")
async def page_list(pageSize: int = 100, pageNum: int = 1):
    if pageNum < 1:
        raise ValueError("页码不能小于1")
    result_list = file_info_db.page_list(None, page_size=pageSize, page_num=pageNum)
    if result_list:
        file_list = [FileInfoVo(file) for file in result_list]
        total_count = file_info_db.get_file_total_count()
        return PageInfo.with_data(total_count=total_count, page_size=pageSize, page_num=pageNum, data_list=file_list)
    else:
        return PageInfo.empty()


@app.get("/getDuplicateList")
async def get_duplicate_list():
    return file_info_db.find_duplicate_file_list()


@app.get("/findByMd5")
async def find_by_md5(md5: str):
    result_list = file_info_db.get_file_by_md5(md5)
    if result_list:
        return [FileInfoVo(file) for file in result_list]
    else:
        return []
