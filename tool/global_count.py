import threading

is_running_file_scan = False
file_total_count = 0
file_scan_count = 0
is_running_file_md5_cal = False
file_md5_total_count = 0
fild_md5_finished_count = 0
is_running_object_detect = False
object_detect_total_count = 0
object_detect_finished_count = 0

scan_flag = True
detect_flag = True
md5_flag = True

detect_lock = threading.Lock()
md5_lock = threading.Lock()


def start_file_md5():
    global md5_flag
    md5_flag = True
    global is_running_file_md5_cal
    is_running_file_md5_cal = True


def stop_file_md5():
    global md5_flag
    md5_flag = False


def finish_file_md5():
    global md5_flag
    md5_flag = False
    global is_running_file_md5_cal
    is_running_file_md5_cal = False


def change_file_md5_count(total: int):
    global file_md5_total_count
    file_md5_total_count = total


def add_file_md5_finished_count():
    with md5_lock:
        global fild_md5_finished_count
        fild_md5_finished_count = fild_md5_finished_count + 1


def start_object_detect():
    global detect_flag
    detect_flag = True
    global is_running_object_detect
    is_running_object_detect = True


def stop_object_detect():
    global detect_flag
    detect_flag = False


def finish_object_detect():
    global detect_flag
    detect_flag = False
    global is_running_object_detect
    is_running_object_detect = False


def change_object_total_count(total: int):
    global object_detect_total_count
    object_detect_total_count = total


def add_object_finished_count():
    with detect_lock:
        global object_detect_finished_count
        object_detect_finished_count = object_detect_finished_count + 1
