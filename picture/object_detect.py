import os.path

from domain import file_info_db, base_config_db, object_detect_db
from picture.yolo import yolo


def start_detect(file_info: file_info_db.FileInfo):
    if not file_info or file_info.file_type != 'pic':
        print("当前图片内容为空，不做处理")
        return
    if not os.path.exists(file_info.file_path):
        print(f"{file_info.file_path}图片不存在，不做处理")
        return
    pic_tmp_path = base_config_db.get_config(base_config_db.ConfigKeyEnum.PIC_TMP_PATH.value)
    pic_tmp_path = os.path.join(pic_tmp_path, f"{file_info.id}")
    if not os.path.exists(pic_tmp_path):
        os.makedirs(pic_tmp_path)
    object_detect_result_list = yolo.detect(file_path=file_info.file_path, tmp_save_path=pic_tmp_path)
    if object_detect_result_list:
        for object_detect_result in object_detect_result_list:
            object_detect_result.id = file_info.id
            object_detect_db.add_object_detect(object_detect_result)
