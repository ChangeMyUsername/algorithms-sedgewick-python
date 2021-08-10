#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from typing import List, Any

from module_1_1 import binary_search


def two_sum_fast(arr: List[Any]) -> int:
    """Count the number of pair of numbers add up to zero. first sort the list,
       then use binary_search the get the other number
       which could add up to zero, if in the list, then increase the counter.

    Args:
        arr (List[Any]): input list, list will be sorted in-place
    Returns:
        int: pair count of two number add up to zero

    >>> arr = [-1, 1, -2, 3, 5, -5, 0, 4]
    >>> two_sum_fast(arr)
    2
    """
    arr.sort()
    cnt = 0
    for i in range(len(arr)):
        if binary_search(-arr[i], arr) > i:
            cnt += 1
    return cnt


def two_sum_with_target(arr: List[Any], target: int) -> tuple[int, int]:
    """Get the first indices of the list which two elements add up to target.
    Can not use the same element twice. Using dictionary to mark the indice
    of the number, if `target` - number in dictionary, return tuple of indices.

    Args:
        arr (List[Any]): [description]
        target (int): [description]

    Returns:
        int: pair of indices, if all numbers not match, then return empty tuple

    >>> arr = [2, 7, 11, 15]
    >>> two_sum_with_target(arr, 9)
    (0, 1)
    >>> arr2 = [3, 3]
    >>> two_sum_with_target(arr2, 6)
    (0, 1)
    >>> arr3 = [3, 2, 4, 1]
    >>> two_sum_with_target(arr3, 6)
    (1, 2)
    """
    num_indexes = {}
    for index, num in enumerate(arr):
        if target - num in num_indexes:
            return (num_indexes[target - num], index)
        num_indexes[num] = index
    return ()


# 1.4.15 practice
def three_sum_fast(arr: List[Any]) -> int:
    """Find four elements that sum to 0. first sort the list,
    then use two for-loop and binary search algorithm get the
    opposite number.

    Args:
        arr (List[Any]): input list

    Returns:
        int: count of how many three numbers add up to zero

    >>> lst = [-1, 2, 1, 3, 0, 4, -4, 5, 9, -5]
    >>> three_sum_fast(lst)
    8
    """
    arr.sort()
    cnt = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if binary_search(-arr[i] - arr[j], arr) > j:
                cnt += 1
    return cnt


# 1.4.14 practice
def four_sum_fast(arr: List[Any]) -> int:
    """Find four elements that sum to 0, store summation of all pair of elements
    in dictionary, then look up the negative summation in dictionary.

    Args:
        arr (List[Any]): input list

    Returns:
        int: the count of four elements sum to 0

    >>> four_sum_fast([1, 0, -1, 0, -2, 2])
    3
    """
    index = {}
    seen = set()
    count = 0

    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            index[arr[i] + arr[j]] = (i, j)

    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            summation = arr[i] + arr[j]
            if -summation in index:
                indexes_tuple = index[-summation]
                fingerprint = tuple(sorted(
                        [i, j, indexes_tuple[0], indexes_tuple[1]]))
                if (indexes_tuple[0] != i and
                    indexes_tuple[0] != j and
                    indexes_tuple[1] != i and
                    indexes_tuple[1] != j and
                        fingerprint not in seen):
                    seen.add(fingerprint)
                    count += 1
    return count


# 1.4.16 practice
def closest_pair(arr: List[Any]) -> tuple[Any, Any]:
    """Get two closest number in a list, first sort the list,
    then iterate through the list compare each
    summation of two adjacent numbers in the list,
    then get the result.

    Args:
        arr (List[Any]): input array

    Returns:
        tuple[Any, Any]: closest pair in array

    >>> lst = [1, 0, 3, 4, 5, 9, 1]
    >>> closest_pair(lst)
    (1, 1)
    >>> lst
    [1, 0, 3, 4, 5, 9, 1]
    """
    sorted_arr = sorted(arr)
    max_val = 9999999999
    a, b = None, None
    for i in range(len(sorted_arr) - 1):
        res = abs(sorted_arr[i] - sorted_arr[i + 1])
        if res < max_val:
            max_val = res
            a, b = sorted_arr[i], sorted_arr[i + 1]
    return a, b


# 1.4.17 practice
def farthest_pair(arr: List[Any]) -> tuple[Any, Any]:
    return min(arr), max(arr)


# 1.4.18 practice
def partial_minimum(lst):
    """
      Find the partial minimum number in the list,
    the whole process is similar to binary search algorithm.
    >>> lst = [5, 2, 3, 4, 3, 5, 6, 8, 7, 1, 9]
    >>> partial_minimum(lst)
    2
    """
    start, end = 0, len(lst) - 1
    while start <= end:
        mid = int((end + start) / 2)
        left = lst[mid - 1]
        right = lst[mid + 1]
        if lst[mid] <= left and lst[mid] <= right:
            return lst[mid]
        if lst[mid] > right and mid + 1 <= end:
            start = mid + 1
        elif lst[mid] > left and mid - 1 >= start:
            end = mid - 1
    return lst[start] if lst[start] < lst[end] else lst[end]


# 1.4.20 practice
def bitonic_list_search(key, lst):
    """
    >>> lst = [1, 2, 3, 9, 8, 7, 6, 5, 4, -1]
    >>> bitonic_list_search(2, lst)
    1
    >>> bitonic_list_search(9, lst)
    3
    >>> bitonic_list_search(7, lst)
    5
    """
    def find_the_point(lst):
        low, high = 0, len(lst) - 1
        while low < high:
            mid = int((low + high) / 2)
            if lst[mid] < lst[mid + 1]:
                low = mid + 1
            elif lst[mid] > lst[mid + 1]:
                high = mid
        return high

    def find_left(key, start, end, lst):
        while start <= end:
            mid = int((start + end) / 2)
            if lst[mid] < key:
                start = mid + 1
            elif lst[mid] > key:
                end = mid - 1
            else:
                return mid
        return -1

    def find_right(key, start, end, lst):
        while start <= end:
            mid = int((start + end) / 2)
            if lst[mid] < key:
                end = mid - 1
            elif lst[mid] > key:
                start = mid + 1
            else:
                return mid
        return -1

    index = find_the_point(lst)
    if key == lst[index]:
        return index
    right = find_right(key, index, len(lst) - 1, lst)
    left = find_left(key, 0, index, lst)
    return left if left > -1 else right


if __name__ == '__main__':
    doctest.testmod()
