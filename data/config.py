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
config_json = {}

with open(config_path, 'r') as f:
    config_json = json.load(f)
