import json
import os

from data import config

process_data = {}


def load_progress():
    if os.path.exists(config.get_file_scan_process_path()):
        with open(config.get_file_scan_process_path(), 'r') as f:
            progress_info = json.load(f)
    else:
        progress_info = {'file_count': 0, 'scanned_dirs': [], 'to_scan_dirs': []}
    global process_data
    process_data = progress_info


def save_process(scan_queue):
    with open(config.get_file_scan_process_path(), 'w') as f:
        global process_data
        process_data['to_scan_dirs'] = list(scan_queue.queue)
        json.dump(process_data, f)


def get_progress():
    return process_data


