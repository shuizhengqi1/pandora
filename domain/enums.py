from enum import Enum


class ConfigKeyEnum(Enum):
    START_DIR = "start_dir"
    SCAN_INTERVAL = "scan_interval"
    SCAN_PROCESS_PATH = "scan_process_path"
    SKIP_DIR_NAME = "skip_dir_name"
    PIC_TMP_PATH = "pic_tmp_path"
    MODEL_PATH = "model_path"


class FaceReconStatus(Enum):
    INIT = 0
    SUCCESS = 1
    FAIL = 2


class MediaTypeEnum(Enum):
    VIDEO = "video"
    PIC = "pic"
    DOCUMENT = "document"


class PicHandleStatus(Enum):
    INIT = 0
    DONE = 1
    WAIT_CON = 2
    ERROR = 3
