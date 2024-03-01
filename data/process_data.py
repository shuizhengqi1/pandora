import json
import os

from domain import base_config_db

process_data = {}


def load_progress():
    path = base_config_db.get_config("scan_process_path")
    if os.path.exists(path):
        with open(path, 'r') as f:
            progress_info = json.load(f)
    else:
        progress_info = {'file_count': 0, 'scanned_dirs': [], 'to_scan_dirs': []}
    global process_data
    process_data = progress_info


def save_process(scan_queue):
    with open(base_config_db.get_config("scan_process_path"), 'w') as f:
        global process_data
        process_data['to_scan_dirs'] = list(scan_queue.queue)
        json.dump(process_data, f)


def get_progress():
    return process_data
