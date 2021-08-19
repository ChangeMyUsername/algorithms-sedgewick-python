#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
from typing import MutableSequence

from collections import deque

from common import CT, BaseSort

INSERTION_SORT_LENGTH = 8


class QuickSort(BaseSort):

    """Quick sort implementation, pick certain element in given array
    as pivot, then put other elements in correct position, elements smaller
    than pivot will be put before pivot, elements larger than pivot will
    be put after pivot. After that, recursively execute partition.

    Original quick sort is not a stable algorithm, there are many factors
    can effect algorithm's performance.

    Quick sort is an in-place algorithm.
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Quick sort main method.

        Args:
            seq (MutableSequence[CT]): input array

        >>> qs = QuickSort()
        >>> seq = [3, 2, 4, 7, 8, 9, 1, 0, 14, 11, 23, 50, 26]
        >>> qs.sort(seq)
        >>> qs.show(seq)
        0 1 2 3 4 7 8 9 11 14 23 26 50
        >>> seq2 = ['E', 'A', 'S', 'Y', 'Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N']
        >>> qs.sort(seq2)
        >>> qs.show(seq2)
        A E E I N O Q S S T U Y
        """
        random.shuffle(seq)
        self.__sort(seq, 0, len(seq) - 1)

    def __sort(self, seq, low, high):
        length = high - low + 1
        if length <= INSERTION_SORT_LENGTH:
            self.insertion_sort(seq, low, high)
            return
        index = self.partition(seq, low, high)
        self.__sort(seq, low, index)
        self.__sort(seq, index + 1, high)

    # 2.3.25 practice
    def insertion_sort(
            self, seq: MutableSequence[CT], low: int, high: int) -> None:
        """Sort smaller array with insertion sort in quick sort algorithm.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        >>> quick_sort = QuickSort()
        >>> sequence = [0, 4, 7, 1, -3, 9]
        >>> quick_sort.insertion_sort(sequence, 0, len(sequence) - 1)
        >>> quick_sort.is_sorted(sequence)
        True
        >>> quick_sort.show(sequence)
        -3 0 1 4 7 9
        """
        for i in range(low + 1, high + 1):
            j = i
            while j > low and seq[j] < seq[j - 1]:
                seq[j], seq[j - 1] = seq[j - 1], seq[j]
                j -= 1

    # 2.3.18 practice
    def three_sample(self, seq: MutableSequence[CT],
                     low: int, mid: int, high: int) -> int:
        """Cherry pick median number of `seq[low]`, `seq[mid]`, `seq[high]`,
        this process can improve quick sort's performance.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): array index from left side
            mid (int): array index in the middle of array
            high (int): array index from right side

        Returns:
            int: index of median number among these three numbers.

        >>> qs = QuickSort()
        >>> seq = [4, 1, 8, 9, 6, -5, 2]
        >>> qs.three_sample(seq, 1, 4, 5) # return low index
        1
        >>> qs.three_sample(seq, 4, 5, 6) # return high index
        6
        >>> qs.three_sample(seq, 3, 4, 5) # return mid index
        4
        """
        if (seq[low] <= seq[mid] <= seq[high] or
                seq[high] <= seq[mid] <= seq[low]):
            return mid
        elif (seq[mid] <= seq[low] <= seq[high] or
                seq[high] <= seq[low] <= seq[mid]):
            return low
        else:
            return high

    # 2.3.19 practice
    def five_sample(
            self, seq: MutableSequence[CT], low: int, high: int) -> int:
        """Cherry pick median number of randomly picked five numbers
        between `low` and `high`.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        Returns:
            int: index of median number of five numbers
        """
        values = []
        for _ in range(5):
            index = random.randint(low, high)
            values.append((index, seq[index]))
        values.sort(key=lambda item: item[1])
        return values[2][0]

    def partition(self, seq: MutableSequence[CT], low: int, high: int) -> int:
        """Quick sort partition process, return pivot's changed position
        after partition.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        Returns:
            int: index of pivot
        """
        # length = high - low + 1
        # index = self.three_sample(lst, low, low + length / 2, high)
        index = self.five_sample(seq, low, high)
        seq[low], seq[index] = seq[index], seq[low]
        i, j = low + 1, high
        val = seq[low]
        while 1:
            while i < high and seq[i] <= val:
                i += 1
            while j > low and seq[j] >= val:
                j -= 1
            if i >= j:
                break
            seq[i], seq[j] = seq[j], seq[i]

        seq[low], seq[j] = seq[j], seq[low]
        return j


# 2.3.20
class QuickSortNonRecursive(BaseSort):

    """Quick sort non-recursive version.
    """

    def five_sample(
            self, seq: MutableSequence[CT], low: int, high: int) -> int:
        """Cherry pick median number of randomly picked five numbers
        between `low` and `high`.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        Returns:
            int: index of median number of five numbers
        """
        values = []
        for _ in range(5):
            index = random.randint(low, high)
            values.append((index, seq[index]))
        values.sort(key=lambda item: item[1])
        return values[2][0]

    def partition(self, seq: MutableSequence[CT], low: int, high: int) -> int:
        """Quick sort partition process, return pivot's changed position
        after partition.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        Returns:
            int: index of pivot
        """
        index = self.five_sample(seq, low, high)
        seq[low], seq[index] = seq[index], seq[low]
        i, j = low + 1, high
        val = seq[low]
        while 1:
            while i < high and seq[i] <= val:
                i += 1
            while j > low and seq[j] >= val:
                j -= 1
            if i >= j:
                break
            seq[i], seq[j] = seq[j], seq[i]

        seq[low], seq[j] = seq[j], seq[low]
        return j

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Quick sort main method

        Args:
            seq (MutableSequence[CT]): input array

        >>> qs = QuickSortNonRecursive()
        >>> seq = [3, 2, 4, 7, 8, 9, 1, 0, 14, 11, 23, 50, 26]
        >>> qs.sort(seq)
        >>> qs.show(seq)
        0 1 2 3 4 7 8 9 11 14 23 26 50
        >>> seq2 = ['E', 'A', 'S', 'Y', 'Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N']
        >>> qs.sort(seq2)
        >>> qs.show(seq2)
        A E E I N O Q S S T U Y
        """
        stack = deque()
        stack.append((0, len(seq) - 1))
        while len(stack) > 0:
            low, high = stack.pop()
            if low >= high:
                continue
            index = self.partition(seq, low, high)
            stack.append((index + 1, high))
            stack.append((low, index))


# 2.3.22
class QuickThreeWay(BaseSort):

    """
    >>> qtw = QuickThreeWay()
    >>> lst = [3, 2, 4, 7, 8, 9, 1, 0]
    >>> qtw.sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 7, 8, 9]
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Quick three-way sort implementation.

        Args:
            seq (MutableSequence[CT]): input array

        >>> qs = QuickThreeWay()
        >>> seq = [3, 2, 4, 7, 8, 9, 1, 0, 14, 11, 23, 50, 26]
        >>> qs.sort(seq)
        >>> qs.show(seq)
        0 1 2 3 4 7 8 9 11 14 23 26 50
        >>> seq2 = ['E', 'A', 'S', 'Y', 'Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N']
        >>> qs.sort(seq2)
        >>> qs.show(seq2)
        A E E I N O Q S S T U Y
        """
        random.shuffle(seq)
        self.__sort(seq, 0, len(seq) - 1)

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
