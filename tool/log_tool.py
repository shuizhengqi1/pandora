import time
from functools import wraps


def log_process(name):
    def wrapper(func):
        # 执行函数
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # 函数执行前打印内容
            print(f"{name}-执行")
            result = func(*args, **kwargs)
            # 函数执行后打印内容
            print(f"{name}-执行结束")
            return result

        return inner_wrapper

    return wrapper


def log_duration(name):
    def wrapper(func):
        # 执行函数
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # 函数执行前打印内容
            start_time = time.time()
            result = func(*args, **kwargs)
            # 函数执行后打印内容
            end_time = time.time()
            print(f"{name}耗时:{int((end_time-start_time)*1000)}ms")
            return result
        return inner_wrapper

    return wrapper
