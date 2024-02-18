# plan

1. 需要处理的文件范围：
    1. 文件：名称包含
    2. 图片：包含人脸的图片
    3. 视频：音频或帧包含人脸
2. 需要做的内容
    1. 扫描指定路径下的所有文件，只处理指定部分内容如 doc，pdf，txt，pic 等
    2. 记录每个文件大小，名称，创建时间，修改时间，路径
    3. 文件名称匹配，输出结果
    4. 图片匹配处理，记录结果
    5. 视频分析处理，记录结果
3. 包结构
    1. 文件扫描，存储
    2. 视频处理
        1. 音频提取
            1. 音频识别
        2. 画面匹配（有人脸），记录下来人脸特征，或者提取出来
        3. 视频抽帧，人脸检测
    3. 可读文件读取

图片模块：
1. 图片md5计算，用于进行去重
2. 相似图片对比



环境依赖：
sqlite

文件结构:
config.json:配置文件
db_tools.py:进行表数据的读写
domain/domain_item.py:对象模型定义
file_handle.py: 文件扫描及读取
video/video_handle.py: 视频处理，包括音频提取，视频帧抽取
video/audio_detect.py: 视频音频文件处理，包括人声提取，特征提取
video/video_face_detect.py: 视频人脸识别
picture/face_detect.py:视频人脸识别
data/file_scan_progress.json:文件扫描进度
data/config.py:将config处理成可直接使用的形式