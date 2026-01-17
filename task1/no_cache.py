def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value
