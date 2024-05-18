import os.path
import concurrent.futures

import torch.cuda

from domain import file_info_db, base_config_db, object_detect_db, pic_info_db
from picture.yolo import yolo
from tool.executor_tool import detect_pool
from domain.enums import PicObjectDetectStatus
from tool import global_count


def start_detect(file_info: file_info_db.FileInfo, pic_info: pic_info_db.PicInfo):
    if not global_count.detect_flag:
        print(f"停止检测")
        return
    if not file_info or file_info.file_type != 'pic':
        print("当前图片内容为空，不做处理")
        return
    if not os.path.exists(file_info.file_path):
        print(f"{file_info.file_path}图片不存在，不做处理")
        return
    pic_tmp_path = base_config_db.get_config(base_config_db.ConfigKeyEnum.PIC_TMP_PATH.value)
    pic_tmp_path = os.path.join(pic_tmp_path, f"{file_info.id}")
    # 判断临时路径是否存在
    if not os.path.exists(pic_tmp_path):
        os.makedirs(pic_tmp_path)
    # 先置为待检测状态
    pic_info.object_detect_status = PicObjectDetectStatus.WAIT_CON.value
    pic_info_db.update_object_detect_result(pic_info)
    # 执行检测，获取结果
    object_detect_result_list = yolo.detect(file_path=file_info.file_path, tmp_save_path=pic_tmp_path)
    # 记录结果
    if object_detect_result_list:
        for object_detect_result in object_detect_result_list:
            object_detect_result.file_id = file_info.id
            object_detect_db.add_object_detect(object_detect_result)
    pic_info.object_detect_status = PicObjectDetectStatus.DONE.value
    pic_info_db.update_object_detect_result(pic_info)
    global_count.add_object_finished_count()


async def start_detect_all():
    # 设置个标记位
    global_count.start_object_detect()
    unprocessed_count = pic_info_db.get_pic_need_object_detect_count()
    page_size = 10
    total_page = round(unprocessed_count / page_size)
    global_count.change_object_total_count(unprocessed_count)
    for i in range(total_page):
        if not global_count.detect_flag:
            print(f"停止对象检测")
            return
        future_list = []
        pic_list = pic_info_db.get_to_process_object_detect_list(page_size, i)
        print(f"开始处理第{i}批数据")
        if pic_list:
            for pic_info_domain, file_info_domain in pic_list:
                future_list.append(detect_pool.submit(start_detect, file_info_domain, pic_info_domain))
        for future in concurrent.futures.as_completed(future_list):
            future.result()
    print(f"处理完成，清理缓存")
    global_count.finish_object_detect()
    torch.cuda.empty_cache()
