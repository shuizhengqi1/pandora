import json
import os

from domain import base_config_db

process_data = {}
scan_file_name = "file_scan_progress.json"


def get_progress_file_path():
    path = os.path.join(base_config_db.get_config("scan_process_path"), scan_file_name)
    return path


def load_progress():
    path = get_progress_file_path()
    if os.path.exists(path):
        with open(path, 'r') as f:
            progress_info = json.load(f)
    else:
        progress_info = {'file_count': 0, 'scanned_dirs': [], 'to_scan_dirs': []}
    global process_data
    process_data = progress_info


def save_process(scan_queue):
    path = get_progress_file_path()
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        print(f"生成目录:{dir_name}")
        os.makedirs(dir_name)
        print(f"生成目录:{dir_name}")
    with open(path, 'w') as f:
        global process_data
        process_data['to_scan_dirs'] = list(scan_queue.queue)
        json.dump(process_data, f)


def get_progress():
    return process_data
