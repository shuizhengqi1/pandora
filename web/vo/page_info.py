from typing import Any

from pydantic import BaseModel


class PageInfo(BaseModel):
    totalCount: int
    totalPageCount: int
    pageSize: int
    pageNum: int
    data: list

    def __init__(self, total_count: int, total_page_count: int, page_size: int, page_num: int, data_list: list):
        super().__init__(
            totalCount=total_count,
            totalPageCount=total_page_count,
            pageSize=page_size,
            pageNum=page_num,
            data=data_list
        )

    @classmethod
    def with_data(cls, total_count: int, page_size: int, page_num: int, data_list: list):
        total_page_count = max(1, total_count // page_size) if page_size else 0
        return cls(total_count, total_page_count, page_size, page_num, data_list)

    @classmethod
    def empty(cls):
        return cls(0, 0, 0, 0, [])
