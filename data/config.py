import json
import os

config_path = './data/config.json'
config_json = {}

with open(config_path, 'r') as f:
    config_json = json.load(f)
