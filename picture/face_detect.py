import shutil
import os
from tqdm import tqdm
from domain import pic_info_db, face_info_db, file_info_db
from file import file_md5
import concurrent.futures
import multiprocessing
from picture.pytorch_module.face_detect import Pytorch

save_path = 'face_icon'
num_cores = multiprocessing.cpu_count()

# 检测用的线程池
detect_executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_cores - 1)


def choose_framework(code):
    if code == 'pytorch':
        return Pytorch()
    # if code == "keras":
    # return Keras()


platform = choose_framework("pytorch")


def process_all_pic():
    # pic_info_db.init_all()
    # face_info_db.delete_all()
    total_count = pic_info_db.get_pic_total_count()
    print(f"当前图片总数为{total_count}")
    unprocessed_count = pic_info_db.get_pic_need_detect_count()
    print(f"当前待检测图片总数为{unprocessed_count}")
    if os.path.exists(save_path):
        print(f"当前目录:{save_path}已存在，执行删除")
        shutil.rmtree(save_path)
    page_size = 100
    total_page = round(unprocessed_count / page_size)
    # 记录总共进度
    with tqdm(total=unprocessed_count,
              bar_format="处理百分比：{percentage:3.0f}%|{bar}|已处理{n_fmt}/总数{total_fmt}",
              smoothing=0) as total_bar:
        future_list = []
        for i in range(total_page):
            pic_list = pic_info_db.get_to_process_pic_list(page_size, i)
            if pic_list:
                for pic_info_domain, file_info_domain in pic_list:
                    future_list.append(detect_executor.submit(handle_file, pic_info_domain, file_info_domain))
        for future in concurrent.futures.as_completed(future_list):
            future.result()
            total_bar.update(1)


def handle_file(pic_info_domain: pic_info_db.PicInfo, file_info_domain: file_info_db.FileInfo):
    # 前置检查
    file_info_domain = check_before_detect(file_info_domain)
    # 处理
    detect_face_and_save(pic_info_domain, file_info_domain)


# 人脸检测之前先判断md5是否存在，如果不存在则处理，然后重新查询
def check_before_detect(file_info: file_info_db.FileInfo):
    if file_info.file_md5 == 'tmp':
        print(f"当前文件{file_info.file_path}md5 不存在，开始计算")
        file_md5.calculate_md5(file_id=file_info.id, file_path=file_info.file_path)
        file_info = file_info_db.get_by_id(file_info.id)
    return file_info


# 检测人脸数据，并保存
def detect_face_and_save(pic_info_domain: pic_info_db.PicInfo, file_info_domain: file_info_db.FileInfo):
    face_base_path = os.path.join(save_path, file_info_domain.file_md5)
    try:
        face_list = platform.face_detect(file_info_domain.file_path, face_base_path)
        if face_list:
            # 检测到人脸数据
            pic_info_domain.face_count = len(face_list)
            pic_info_domain.face_icon_path = os.path.abspath(face_base_path)
            pic_info_domain.status = pic_info_db.PicHandleStatus.WAIT_CON.value
            add_face_info(pic_info_domain.id, face_list)
        else:
            pic_info_domain.status = pic_info_db.PicHandleStatus.DONE.value
    except Exception as e:
        print(f"图片{file_info_domain.file_path}检测失败，异常原因:{e}")
        pic_info_domain.status = pic_info_db.PicHandleStatus.ERROR.value
    pic_info_db.update_face_detect_result(pic_info_domain)


def add_face_info(pic_id, face_list):
    for face_path in face_list:
        face_info_db.add_face_info(face_info=face_info_db.FaceInfo(
            pic_id=pic_id,
            face_path=os.path.abspath(face_path),
            status=face_info_db.FaceReconStatus.INIT.value
        ))


