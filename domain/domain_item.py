# -*- coding: utf-8 -*-

from data import config


class FileDomainItem:
    def __init__(self, file_name, file_path, file_size, file_md5, file_suffix, file_create_time, file_modify_time):
        self.file_name = file_name
        self.file_path = file_path
        self.file_size = file_size
        self.file_md5 = file_md5
        self.file_suffix = file_suffix
        self.file_type = config.get_suffix_type(file_suffix)
        self.file_create_time = file_create_time
        self.file_modify_time = file_modify_time


class VideoDomainItem:
    def __init__(self, video_duration, video_audio_path, video_audio_md5):
        self.video_duration = video_duration
        self.video_audio_path = video_audio_path
        self.video_audio_md5 = video_audio_md5
