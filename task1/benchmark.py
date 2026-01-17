import time


def measure_time(func, *args):
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start
