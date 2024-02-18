import json
import os

config_path = './data/config.json'
# -初始化-
# 开始的目录
dir_path = ''
# 文件扫描进度的数据存储
file_scan_process_path = './data/file_scan_progress.json'
suffix_type_map = dict()
skip_dir_name = []

with open(config_path, 'r') as f:
    config = json.load(f)
    if config['start_dir']:
        dir_path = config['start_dir']
    if config['scan_process_path']:
        file_scan_process_path = config['scan_process_path']
    if config['skip_dir_name']:
        skip_dir_name = config['skip_dir_name']
    if config['type_map']:
        config_type_map = config['type_map']
        for key in config_type_map:
            for value in config_type_map[key]:
                suffix_type_map[value] = key
    print('配置文件加载完毕')
    print(suffix_type_map)


def get_skip_dir_name():
    return skip_dir_name


def get_suffix_type(suffix):
    return suffix_type_map[suffix.lower()]


def get_dir_path():
    return dir_path


def get_file_scan_process_path():
    return file_scan_process_path


def get_suffix_list():
    return list(suffix_type_map.keys())


def remove_process():
    return True
