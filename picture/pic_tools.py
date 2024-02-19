# -*- coding: utf-8 -*-

import hashlib
import time
import db.db_tools as db_tools
from tqdm import tqdm
from db.file_info import FileInfo


def cal_all_pic():
    total_count = db_tools.query_total_count('document')
    print(f"总数是{total_count}")
    total_bar = tqdm(total_count)
    flag = True
    while flag:
        rowList = db_tools.query_unprocessed_list('document')
        if not rowList:
            flag = False
        for row in rowList:
            try:
                _id = row.id
                file_path = row.file_path
                total_bar.write(f"当前处理:{file_path}")
                md5_value, time_taken = calculate_md5(file_path)
                db_tools.update_file_md5(_id, md5_value)
                total_bar.update(1)
                # print(f"耗时 :{time_taken}")
            except Exception as e:
                print(f"文件扫描异常: {e}")
                continue
    total_bar.close()


def calculate_md5(file_path):
    start_time = time.time()
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_md5.update(chunk)
    end_time = time.time()  # 结束计时
    elapsed_time = end_time - start_time  # 计算耗时
    return hash_md5.hexdigest(), elapsed_time
