from db.db_tools import drop_table
from file import file_handle,file_md5


def run_file_scan():
    drop_table()
    file_handle.get_file_list()


def run_md5_cal():
    file_md5.cal_all_md5()


if __name__ == '__main__':
    run_md5_cal()
