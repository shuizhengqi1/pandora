# -*- coding: utf-8 -*-

import hashlib
import time
import db.db_tools as db_tools


def cal_all_pic():
    rowList = db_tools.query_pic_list()
    while rowList:
        for row in rowList:
            try:
                id = row[0]
                file_path = row[1]
                md5_value, time_taken = calculate_md5(file_path)
                db_tools.update_file_md5(id, md5_value)
                print("耗时 :{}", time_taken)
            except Exception as e:
                print(f"Error scanning directory: {e}")
                continue
        rowList = db_tools.query_pic_list()


def calculate_md5(file_path):
    print(f"cal file:{file_path}")
    start_time = time.time()
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_md5.update(chunk)
    end_time = time.time()  # 结束计时
    elapsed_time = end_time - start_time  # 计算耗时
    return hash_md5.hexdigest(), elapsed_time

