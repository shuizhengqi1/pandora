# -*- coding: utf-8 -*-

import hashlib
import time
import db.db_tools as db_tools


def cal_all_pic():
    rowList = db_tools.get_all_pic()
    for row in rowList:
        try:
            file_path = row[0]
            md5_value, time_taken = calculate_md5(file_path)
            db_tools.update_md5(file_path, md5_value)
            print("耗时 :{}", time_taken)
        except Exception as e:
            continue


def calculate_md5(file_path):
    start_time = time.time()
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1), b""):
            hash_md5.update(chunk)
    end_time = time.time()  # 结束计时
    elapsed_time = end_time - start_time  # 计算耗时
    return hash_md5.hexdigest(), elapsed_time


md5_value, time_taken = calculate_md5('/Users/yanghengxing/Pictures/WechatIMG14691.jpeg')
print(md5_value)
print("耗时 :{}", time_taken)
