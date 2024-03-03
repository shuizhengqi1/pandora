# -*- coding: utf-8 -*-
import hashlib
import os
import sys
import time
from tqdm import tqdm
from domain import file_info_db


def cal_all_md5():
    sys.stdout.write("\033[F\033[K")
    sys.stdout.write("\033[F\033[K")
    sys.stdout.write("\033[F\033[K")
    total_count = file_info_db.query_need_cal_md5_count()
    print(f"总数是{total_count}")
    with tqdm(total=total_count,
              bar_format="处理百分比：{percentage:3.0f}%|{bar}|已处理{n_fmt}/总数{total_fmt}",
              smoothing=0) as total_bar:
        flag = True
        while flag:
            rowList = file_info_db.query_unprocessed_file_list()
            if not rowList:
                flag = False
            for row in rowList:
                try:
                    file_id = row.id
                    file_path = row.file_path
                    sys.stdout.write("\033[F\033[K")
                    total_bar.write(f"当前处理:{file_path}")
                    calculate_md5(file_id, file_path)
                    total_bar.update(1)
                    sys.stdout.write("\033[F\033[K")
                    sys.stdout.flush()
                except Exception as e:
                    print(f"文件扫描异常: {e}")
                    continue


def get_count_info():
    file_count = file_info_db.get_file_total_count()
    need_cal_md5_file_count = file_info_db.query_need_cal_md5_count()
    return file_count, need_cal_md5_file_count


def calculate_md5(file_id, file_path):
    start_time = time.time()
    hash_md5 = hashlib.md5()
    file_size = os.stat(file_path).st_size
    with open(file_path, "rb") as f, tqdm(total=file_size,
                                          bar_format="文件读取进度：{percentage:3.0f}%|{bar}|已处理{n_fmt}/总数{total_fmt}",
                                          smoothing=0) as file_bar:
        batch_size = 8192
        for chunk in iter(lambda: f.read(batch_size), b""):
            hash_md5.update(chunk)
            file_bar.update(batch_size)
    end_time = time.time()  # 结束计时
    elapsed_time = end_time - start_time  # 计算耗时
    file_info_db.update_file_md5(file_id, hash_md5.hexdigest())
    return elapsed_time
