from db.db_tools import drop_table, init_db
from file import file_handle, file_md5
from picture import face_detect
from tool import log_tool
from domain import file_info_db


@log_tool.log_process("文件扫描")
def run_file_scan():
    drop_table()
    init_db()
    file_handle.get_file_list()


@log_tool.log_process("md5计算")
def run_md5_cal():
    file_md5.cal_all_md5()


if __name__ == '__main__':
    # file_info.find_duplicate_file_list()
    # run_file_scan()
    # run_md5_cal()
    face_detect.process_all_pic()
