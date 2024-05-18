from domain import face_info_db, pic_info_db
from tqdm import tqdm
from picture.pytorch_module.face_detect import Pytorch
import multiprocessing
import concurrent.futures
from tool.executor_tool import detect_pool

num_cores = multiprocessing.cpu_count()

platform = Pytorch()


def start_recon():
    total_count = face_info_db.get_face_total_count()
    print(f"当前图片总数为{total_count}")
    unprocessed_count = face_info_db.get_face_need_process_count()
    print(f"当前待检测图片总数为{unprocessed_count}")
    page_size = 100
    total_page = round(unprocessed_count / page_size)

    with tqdm(total=unprocessed_count, bar_format="处理百分比：{percentage:3.0f}%|{bar}|已处理{n_fmt}/总数{total_fmt}",
              smoothing=0) as total_bar:
        future_list = []
        for i in range(total_page):
            face_info_list = face_info_db.get_to_process_face_list(page_size, i)
            if face_info_list:

                for face_info in face_info_list:
                    future_list.append(detect_pool.submit(face_recon, face_info))
        for future in concurrent.futures.as_completed(future_list):
            future.result()
            total_bar.update(1)


def face_recon(face_info: face_info_db.FaceInfo):
    face_feature = platform.face_recon(face_info.face_path)
    if face_feature:
        face_info.status = face_info_db.FaceReconStatus.SUCCESS.value
        face_info.face_feature = face_feature
    else:
        face_info.status = face_info_db.FaceReconStatus.FAIL.value
    face_info_db.update_face_info(face_info)
