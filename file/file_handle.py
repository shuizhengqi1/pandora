# -*- coding: utf-8 -*-
import json
import os
import queue
import sys
import time

import data.config as config
import db.db_tools as db_tools
from db.file_info import FileInfo
import datetime
from data import process_data
import threading

_scanFlag = True
_scanStartTime = 0
_scanCurrentDir = ""
_scanDirCount = 0


def print_progress():
    print("\n\n")
    while _scanFlag:
        # 为了保证能在同一行的位置进行刷新，避免不停的刷屏
        # 清除当前行并将光标移动到第一行开头
        sys.stdout.write("\033[F\033[K")
        # 清除下一行并将光标移动到第二行开头
        sys.stdout.write("\033[F\033[K")
        print(
            f"扫描中，当前已经执行了{int(time.time() - _scanStartTime)}秒，处理了{process_data.get_progress()['file_count']}个文件")
        print(f"当前正在读取文件夹{_scanCurrentDir} 已经扫描完成了{_scanDirCount} 个文件夹")
        time.sleep(2)


# 是否隐藏的文件夹
def skip_dir(directory):
    return '.' in os.path.basename(directory) or os.path.basename(directory) in config.get_skip_dir_name()


# 是否需要处理文件
def filter_need_handle(file_name):
    _, ext = os.path.splitext(file_name)
    return ext.lower() in config.get_suffix_list()


# 具体处理文件的代码
def handle_file(file_path):
    # print("开始处理文件：" + file_path)
    file_info = os.stat(file_path)
    file_name = os.path.basename(file_path)
    file_suffix = os.path.splitext(file_name)[1]
    file_size = round(file_info.st_size / (1024 * 1024), 1)
    create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).replace(microsecond=0)
    modify_time = datetime.datetime.fromtimestamp(file_info.st_mtime).replace(microsecond=0)
    file_domain = FileInfo(
        file_path=file_path,
        file_name=file_name,
        file_suffix=file_suffix,
        file_size=file_size,
        file_type=config.get_suffix_type(file_suffix),
        create_time=create_time,
        modify_time=modify_time
    )
    db_tools.add_file_info(file_domain)


# 扫描文件夹内容
def scan_directory(directory):
    scan_queue = queue.Queue()
    progress_info = process_data.get_progress()
    # 初始化队列
    for dir_path in progress_info['to_scan_dirs']:
        scan_queue.put(dir_path)
    scan_queue.put(directory)

    while not scan_queue.empty():

        current_dir = scan_queue.get()
        # if current_dir in progress_info['scanned_dirs']:
        #     continue
        global _scanDirCount
        global _scanCurrentDir
        _scanCurrentDir = current_dir
        _scanDirCount += 1
        if skip_dir(current_dir):
            continue
        try:
            for entry in os.scandir(current_dir):
                if entry.is_symlink() or not os.access(entry.path, os.R_OK):
                    continue
                if entry.is_file() and filter_need_handle(entry.name):
                    # sys.stdout.write("\033[2J\033[H")
                    # sys.stdout.write(f"已扫描文件个数：{progress_info['file_count']} \r\n")
                    # sys.stdout.write(f"扫描到文件：{entry.path}\n")
                    sys.stdout.flush()
                    handle_file(entry.path)
                    progress_info['file_count'] += 1
                elif entry.is_dir():
                    scan_queue.put(entry.path)
                    # print('扫描到目录：' + entry.path)
                    progress_info['scanned_dirs'].append(entry.path)
                    process_data.save_process(scan_queue)
        except OSError as e:
            print(f"Error scanning directory: {e}")


def init_scan_thread(directory):
    scan_thread = threading.Thread(target=scan_directory, args=directory)
    scan_thread.start()
    return scan_thread


def init_print_thread():
    print_thread = threading.Thread(target=print_progress)
    print_thread.daemon = True
    print_thread.start()


def get_file_list():
    # 删除保存的进度
    if config.remove_process and os.path.exists(config.get_file_scan_process_path()):
        os.remove(config.get_file_scan_process_path())
    # 初始化db
    db_tools.init_db()
    process_data.load_progress()
    # 初始化路径
    origin_path = config.get_dir_path()
    if not origin_path:
        print('请先设置目录路径')
        exit()
    print('开始扫描目录：' + origin_path)
    global _scanStartTime
    _scanStartTime = time.time()
    # 加载进度
    init_print_thread()
    scan_thread = init_scan_thread(origin_path)
    scan_thread.join()
    # 设置全局标记位
    global _scanFlag
    _scanFlag = False

    # 清除当前行并将光标移动到第一行开头
    sys.stdout.write("\033[F\033[K")
    # 清除下一行并将光标移动到第二行开头
    sys.stdout.write("\033[F\033[K")
    print(
        f"处理完成，共计耗时{int(time.time() - _scanStartTime)}秒 处理了{process_data.get_progress()['file_count']}个文件，扫描了{_scanDirCount} 个文件夹 \n")
