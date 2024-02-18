from file import file_handle
from picture import pic_tools


def run_file_scan():
    file_handle.get_file_list()


def run_md5_cal():
    pic_tools.cal_all_pic()


if __name__ == '__main__':
    run_md5_cal()
