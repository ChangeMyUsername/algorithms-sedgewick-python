#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


def selection_sort(lst):
    """
      Selection sort implemention, select the minimum value in the list and put it in first place,
    then scan the whole list but exclude the first one element,
    pick the second minimum value in the list and so on util the list is sorted.
    every selection sort need N TIMES EXCHANGES,
    and the running time is NOTHING TO DO WITH the size of the input array.
    >>> lst = [9, 4, 5, 1, 0, 3, 6]
    >>> selection_sort(lst)
    >>> lst
    [0, 1, 3, 4, 5, 6, 9]
    """
    length = len(lst)
    for i in range(length):
        min_index = i
        for j in range(i + 1, length):
            if lst[j] < lst[min_index]:
                min_index = j
        lst[min_index], lst[i] = lst[i], lst[min_index]


def insertion_sort(lst):
    """
      Insertion sort implementation, exchange the current element
    and the previous element util current element is larger than the previous element.
    for a random list of N size, insertion sort need ~ N**2/4 comparisons
    and ~N**2/4 exchanges on average condition,
    the worst-case scenario would be ~ N**2/2 comparisons and ~N**2/2 exchanges,
    the best-case scenario would be N-1
    comparisons and no exchange.
    >>> lst = [9, 4, 5, 1, 0, 3, 6]
    >>> insertion_sort(lst)
    >>> lst
    [0, 1, 3, 4, 5, 6, 9]
    """
    length = len(lst)
    for i in range(1, length):
        j = i
        while j and lst[j] < lst[j - 1]:
            lst[j], lst[j - 1] = lst[j - 1], lst[j]
            j -= 1


def shell_sort(lst):
    """
      Shell sort implementation, exchange the j element
    and j-h element util i element is larger than i-1 element.
    the algorithms performance is depend on h
    >>> lst = [9, 4, 5, 1, 0, 3, 6]
    >>> shell_sort(lst)
    >>> lst
    [0, 1, 3, 4, 5, 6, 9]
    """
    length = len(lst)
    h = 1

    while h < length / 3:
        h = 3 * h + 1

    while h >= 1:
        for i in range(h, length):
            j = i
            while j >= h and lst[j] < lst[j - h]:
                lst[j], lst[j - h] = lst[j - h], lst[j]
                j -= h
        h //= 3

if __name__ == '__main__':
    doctest.testmod()
