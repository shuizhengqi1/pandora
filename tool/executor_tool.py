from concurrent.futures import ThreadPoolExecutor
import atexit

file_pool = ThreadPoolExecutor(max_workers=5)
api_pool = ThreadPoolExecutor(max_workers=10)


def clean():
    print("关闭线程池")
    file_pool.shutdown(wait=False)
    api_pool.shutdown(wait=False)
