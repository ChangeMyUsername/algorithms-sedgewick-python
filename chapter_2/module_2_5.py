#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


def rank(lst, k):
    '''
    >>> rank([i for i in range(10)], 5)
    4
    '''
    def partition(lst, low, high):
        val = lst[low]
        left, right = low, high
        while 1:
            while lst[left] < val:
                left += 1
            while lst[right] > val:
                right -= 1
            if right < left:
                break
            lst[left], lst[right] = lst[right], lst[left]
        lst[left], lst[low] = lst[low], lst[left]
        return left
    low, high = 0, len(lst) - 1
    while high > low:
        j = partition(lst, low, high)
        if j == k:
            return lst[k]
        elif j > k:
            high = j - 1
        elif j < k:
            low = j + 1
    return lst[k]


if __name__ == '__main__':
    doctest.testmod()
