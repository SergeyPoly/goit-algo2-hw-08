import random

from lru_cache import LRUCache
from queries import make_queries
from no_cache import range_sum_no_cache, update_no_cache
from with_cache import range_sum_with_cache, update_with_cache
from benchmark import measure_time


def run_no_cache(array, queries):
    for q in queries:
        if q[0] == "Range":
            _, l, r = q
            range_sum_no_cache(array, l, r)
        else:
            _, idx, val = q
            update_no_cache(array, idx, val)


def run_with_cache(array, queries):
    cache = LRUCache(capacity=1000)
    for q in queries:
        if q[0] == "Range":
            _, l, r = q
            range_sum_with_cache(array, l, r, cache)
        else:
            _, idx, val = q
            update_with_cache(array, idx, val, cache)


if __name__ == "__main__":
    N = 100_000
    Q = 50_000

    base_array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    arr1 = base_array.copy()
    t1 = measure_time(run_no_cache, arr1, queries)

    arr2 = base_array.copy()
    t2 = measure_time(run_with_cache, arr2, queries)

    speedup = t1 / t2 if t2 > 0 else float("inf")

    print(f"Без кешу : {t1:6.2f} c")
    print(f"LRU-кеш  : {t2:6.2f} c  (прискорення ×{speedup:.1f})")
