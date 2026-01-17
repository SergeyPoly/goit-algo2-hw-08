from lru_cache import LRUCache


def range_sum_with_cache(array, left, right, cache: LRUCache):
    key = (left, right)
    cached = cache.get(key)
    if cached != -1:
        return cached

    result = sum(array[left : right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache: LRUCache):
    array[index] = value

    keys_to_delete = []
    for l, r in cache.cache.keys():
        if l <= index <= r:
            keys_to_delete.append((l, r))

    for key in keys_to_delete:
        del cache.cache[key]
