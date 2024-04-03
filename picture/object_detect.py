import os.path

from domain import base_config_db
from domain import file_info_db
from picture.yolo import yolo


def start_detect(file_info: file_info_db.FileInfo):
    if not file_info or file_info.file_type != 'pic':
        print("当前图片内容为空，不做处理")
        return
    pic_tmp_path = base_config_db.get_config(base_config_db.ConfigKeyEnum.PIC_TMP_PATH.value)
    pic_tmp_path = os.path.join(pic_tmp_path, file_info.id)
    object_detect_result = yolo.detect(file_path=file_info.file_path, tmp_save_path=pic_tmp_path)
    print(object_detect_result)
