# -*- coding: utf-8 -*-
import hashlib
import sys
import time
import db.db_tools as db_tools
from tqdm import tqdm


def cal_all_md5():
    for _type in ['document', 'pic', 'video']:
        sys.stdout.write("\033[F\033[K")
        sys.stdout.write("\033[F\033[K")
        sys.stdout.write("\033[F\033[K")
        print(f"当前开始处理:{_type}")
        total_count = db_tools.query_total_count(_type)
        print(f"总数是{total_count}")
        total_bar = tqdm(total_count)
        flag = True
        while flag:
            rowList = db_tools.query_unprocessed_list(_type)
            if not rowList:
                flag = False
            for row in rowList:
                try:
                    _id = row.id
                    file_path = row.file_path
                    sys.stdout.write("\033[F\033[K")
                    total_bar.write(f"当前处理:{file_path}")
                    md5_value, time_taken = calculate_md5(file_path)
                    db_tools.update_file_md5(_id, md5_value)
                    total_bar.update(1)
                    sys.stdout.write("\033[F\033[K")
                    print(f"md5计算耗时 :{int(time_taken)}秒")
                    sys.stdout.flush()
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
