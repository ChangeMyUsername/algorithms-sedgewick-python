#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random


INSERTION_SORT_LENGTH = 8


class QuickSort(object):

    """
    >>> qs = QuickSort()
    >>> lst = [3, 2, 4, 7, 8, 9, 1, 0, 14, 11, 23, 50, 26]
    >>> qs.sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 7, 8, 9, 11, 14, 23, 26, 50]
    >>> lst2 = ['E', 'A', 'S', 'Y', 'Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N']
    >>> qs.sort(lst2)
    >>> lst2
    ['A', 'E', 'E', 'I', 'N', 'O', 'Q', 'S', 'S', 'T', 'U', 'Y']
    """

    def sort(self, lst):
        random.shuffle(lst)
        self.__sort(lst, 0, len(lst) - 1)

    def __sort(self, lst, low, high):
        length = high - low + 1
        if length <= INSERTION_SORT_LENGTH:
            self.insertion_sort(lst, low, high)
            return
        index = self.partition(lst, low, high)
        self.__sort(lst, low, index)
        self.__sort(lst, index + 1, high)

    def insertion_sort(self, lst, low, high):
        for i in range(low + 1, high + 1):
            j = i
            while j > low and lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
                j -= 1

    # 2.3.18 practice
    def three_sample(self, lst, low, mid, high):
        if lst[low] <= lst[mid] <= lst[high] or lst[high] <= lst[mid] <= lst[low]:
            return mid
        elif lst[mid] <= lst[low] <= lst[high] or lst[high] <= lst[low] <= lst[mid]:
            return low
        else:
            return high

    # 2.3.19 practice
    def five_sample(self, lst, low, high):
        values = []
        for _ in range(5):
            index = random.randint(low, high)
            values.append((index, lst[index]))
        values.sort(key=lambda item: item[1])
        return values[2][0]

    def partition(self, lst, low, high):
        # length = high - low + 1
        # index = self.three_sample(lst, low, low + length / 2, high)
        index = self.five_sample(lst, low, high)
        lst[low], lst[index] = lst[index], lst[low]
        i, j = low + 1, high
        val = lst[low]
        while 1:
            while i < high and lst[i] <= val:
                i += 1
            while j > low and lst[j] >= val:
                j -= 1
            if i >= j:
                break
            lst[i], lst[j] = lst[j], lst[i]

        lst[low], lst[j] = lst[j], lst[low]
        return j


class QuickThreeWay(object):

    """
    >>> qtw = QuickThreeWay()
    >>> lst = [3, 2, 4, 7, 8, 9, 1, 0]
    >>> qtw.sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 7, 8, 9]
    """

    def sort(self, lst):
        random.shuffle(lst)
        self.__sort(lst, 0, len(lst) - 1)

    def __sort(self, lst, low, high):
        if high <= low:
            return

        lt, i, gt, val = low, low + 1, high, lst[low]
        while i <= gt:
            if lst[i] < val:
                lst[lt], lst[i] = lst[i], lst[lt]
                lt += 1
                i += 1
            elif lst[i] > val:
                lst[gt], lst[i] = lst[i], lst[gt]
                gt -= 1
            else:
                i += 1
        self.__sort(lst, low, lt - 1)
        self.__sort(lst, gt + 1, high)


if __name__ == '__main__':
    doctest.testmod()
