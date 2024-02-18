# -*- coding: utf-8 -*-
import json
import os
import queue
import data.config as config
from domain.domain_item import FileDomainItem
import db.db_tools as db_tools


# 保存进度
def save_process(process_data, scan_queue):
    with open(config.get_file_scan_process_path(), 'w') as f:
        process_data['to_scan_dirs'] = list(scan_queue.queue)
        json.dump(process_data, f)


# 获取进度
def load_progress():
    if os.path.exists(config.get_file_scan_process_path()):
        with open(config.get_file_scan_process_path(), 'r') as f:
            progress_info = json.load(f)
    else:
        progress_info = {'file_count': 0, 'scanned_dirs': [], 'to_scan_dirs': []}
    return progress_info


def get_file_list():
    origin_path = config.get_dir_path()
    if not origin_path:
        print('请先设置目录路径')
        exit()
    print('开始扫描目录：' + origin_path)

    # 加载进度
    progress_info = load_progress()
    scan_directory(origin_path, progress_info)


# 是否隐藏的文件夹
def skip_dir(directory):
    return '.' in os.path.basename(directory) or os.path.basename(directory) in config.get_skip_dir_name()


# 是否需要处理文件
def filter_need_handle(file_name):
    _, ext = os.path.splitext(file_name)
    return ext.lower() in config.get_suffix_list()


def hanle_file(file_path):
    print("开始处理文件：" + file_path)
    file_info = os.stat(file_path)
    file_name = os.path.basename(file_path)
    file_suffix = os.path.splitext(file_name)[1]
    file_size = round(file_info.st_size / (1024 * 1024), 1)
    # file_md5 = get_file_md5(file_path)
    create_time = int(os.path.getctime(file_path))
    modify_time = int(file_info.st_mtime)

    domainItem = FileDomainItem(file_name, file_path, file_size, 'tmp', file_suffix, create_time, modify_time)
    db_tools.add_file_info(domainItem)


# 扫描文件夹内容
def scan_directory(directory, progress_info):
    scan_queue = queue.Queue()
    # 初始化队列
    for dir_path in progress_info['to_scan_dirs']:
        scan_queue.put(dir_path)
    scan_queue.put(directory)

    while not scan_queue.empty():
        current_dir = scan_queue.get()
        if current_dir in progress_info['scanned_dirs']:
            continue
        if skip_dir(directory):
            return
        try:
            for entry in os.scandir(directory):
                if (entry.is_symlink()):
                    continue
                if entry.is_file() and filter_need_handle(entry.name):
                    print('扫描到文件：' + entry.path)
                    print("已扫描文件个数: {}".format(progress_info['file_count']))
                    hanle_file(entry.path)
                    progress_info['file_count'] += 1
                elif entry.is_dir():
                    scan_queue.put(entry.path)
                    # print('扫描到目录：' + entry.path)
                    scan_directory(entry.path, progress_info)
        except OSError as e:
            print(f"Error scanning directory: {e}")

        progress_info['scanned_dirs'].append(current_dir)
        save_process(progress_info, scan_queue)


# 删除进度
if (config.remove_process and os.path.exists(config.get_file_scan_process_path())):
    os.remove(config.get_file_scan_process_path())
    db_tools.drop_db()

# 初始化db
db_tools.init_db()
# 加载计时器
get_file_list()
