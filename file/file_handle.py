# -*- coding: utf-8 -*-
import json
import os
import queue
import sys
import time

from domain import file_info_db, pic_info_db, video_info_db, base_config_db, media_type_db, FileInfo
import datetime
from data import process_data
from tool import executor_tool

_scanFlag = True
_scanStartTime = 0
_scanCurrentDir = ""
_scanDirCount = 0

exist_data = set()


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
    skip_dir_name_list = json.loads(base_config_db.get_config("skip_dir_name"))
    return '.' in os.path.basename(directory) or os.path.basename(directory) in skip_dir_name_list


# 是否需要处理文件
def filter_need_handle(file_path, file_name):
    _, ext = os.path.splitext(file_name)
    return file_path + "-" + file_name not in exist_data and ext.lower() in media_type_db.get_all_suffix()


# 具体处理文件的代码
def handle_file(file_path):
    print("开始处理文件：" + file_path)
    file_info_stat = os.stat(file_path)
    file_name = os.path.basename(file_path)
    file_suffix = os.path.splitext(file_name)[1]
    file_size = round(file_info_stat.st_size / (1024 * 1024), 1)
    create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).replace(microsecond=0)
    modify_time = datetime.datetime.fromtimestamp(file_info_stat.st_mtime).replace(microsecond=0)
    file_info_domain = file_info_db.FileInfo(
        file_path=file_path,
        file_name=file_name,
        file_suffix=file_suffix,
        file_size=file_size,
        file_type=media_type_db.get_media_type_by_suffix(file_suffix),
        create_time=create_time,
        modify_time=modify_time
    )
    file_id = file_info_db.add_file_info(file_info_domain)
    # 记入picInfo数据
    if media_type_db.get_media_type_by_suffix(file_suffix) == 'pic':
        pic_info_db.add_pic_info(pic_info_db.PicInfo(
            file_id=file_id
        ))
    # 记入videoInfo数据
    if media_type_db.get_media_type_by_suffix(file_suffix) == 'video':
        video_info_db.add_video_info(video_info_db.VideoInfo(
            file_id=file_id
        ))


# 扫描文件夹内容
def scan_directory(directory):
    scan_queue = queue.Queue()
    progress_info = process_data.get_progress()
    # 初始化队列
    for dir_path in progress_info['to_scan_dirs']:
        scan_queue.put(dir_path)
    print(f"初始化任务")
    scan_queue.put(directory)
    print(f"初始化队列完成")
    while not scan_queue.empty():
        current_dir = scan_queue.get()
        print(f"当前目录是:{current_dir}")
        global _scanDirCount
        global _scanCurrentDir
        _scanCurrentDir = current_dir
        _scanDirCount += 1
        if skip_dir(current_dir):
            continue
        try:
            print(f"开始获取文件夹数量")
            with os.scandir(current_dir) as scan_it:
                for entry in scan_it:
                    print(f"开始扫描")
                    if entry.is_symlink() or not os.access(entry.path, os.R_OK):
                        continue
                    if entry.is_file() and filter_need_handle(entry.path, entry.name):
                        sys.stdout.flush()
                        handle_file(entry.path)
                        progress_info['file_count'] += 1
                    elif entry.is_dir():
                        scan_queue.put(entry.path)
                        progress_info['scanned_dirs'].append(entry.path)
                        process_data.save_process(scan_queue)
        except OSError as e:
            print(f"Error scanning directory: {e}", e)
            import traceback
            traceback.print_exc()
        # 设置全局标记位
    global _scanFlag
    _scanFlag = False
    print("扫描完成")


def get_file_list():
    process_path = process_data.get_progress_file_path()
    # 删除保存的进度
    if os.path.exists(process_path):
        os.remove(process_path)
    process_data.load_progress()
    # 初始化路径
    origin_path = base_config_db.get_config("start_dir").replace("\\\\", "\\")
    if not origin_path:
        print('请先设置目录路径')
        exit()
    print('开始扫描目录：' + origin_path)
    # 加载已经扫描过的数据
    exist_data_list = file_info_db.get_all_data()
    if exist_data_list:
        for item in exist_data_list:
            exist_data.add(item.file_path + "-" + item.file_name)

    global _scanStartTime
    _scanStartTime = time.time()
    # 加载进度
    # executor_tool.file_pool.submit(print_progress)
    executor_tool.file_pool.submit(scan_directory, origin_path)
    executor_tool.file_pool.join()

    # 清除当前行并将光标移动到第一行开头
    sys.stdout.write("\033[F\033[K")
    # 清除下一行并将光标移动到第二行开头
    print(
        f"处理完成，共计耗时{int(time.time() - _scanStartTime)}秒 处理了{process_data.get_progress()['file_count']}个文件，扫描了{_scanDirCount} 个文件夹 \n")


def file_delete(file: FileInfo):
    if not file:
        raise ValueError("要删除的文件对象不能为空")
    if not os.path.exists(file.file_path):
        print(f"要删除的文件:{file.file_path}不存在，不做处理")
        return
    if not os.path.isfile(file.file_path):
        print(f"要删除的文件:{file.file_path}不是文件，不做处理")
        return
    try:
        os.remove(file.file_path)
        print(f"文件{file.file_path}删除成功")
        file_info_db.delete_by_id_list([file.id])
    except OSError as e:
        print(f"删除文件 {file.file_path} 时出错: {e}")
