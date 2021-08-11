#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from typing import MutableSequence

from common import CT, BaseSort


class SelectionSort(BaseSort):

    """Selection sort implementation
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Selection sort algorithm, sorts an array by repeatedly finding
        the minimum element (considering ascending order) from
        unsorted part and putting it at the beginning.

        Selection sort is stable algorithm.
        Time Complexity is O(n^2).
        It uses ϴ(1) extra memory (not including the input array).

        Args:
            seq (MutableSequence[CT]): mutable sequence

        >>> seq = [9, 4, 5, 1, 0, 3, 6]
        >>> selection_sort = SelectionSort()
        >>> selection_sort.sort(seq)
        >>> selection_sort.is_sorted(seq)
        True
        >>> selection_sort.show(seq)
        0 1 3 4 5 6 9
        """
        length = len(seq)
        for i in range(length):
            min_index = i
            for j in range(i + 1, length):
                if seq[j] < seq[min_index]:
                    min_index = j
            self.exch(seq, min_index, i)


class InsertionSort(BaseSort):

    """Insertion sort implementation
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Insertion sort algorithm, it takes three steps to execute:

        1: Iterate from seq[1] to seq[n] over the sequence.

        2: Compare the current element (key) to its predecessor.

        3: If the key element is smaller than its predecessor,
           compare it to the elements before.
           Move the greater elements one position up
           to make space for the swapped element.

        Insertion sort is stable algorithm.
        Time Complexity is O(n^2).
        It uses ϴ(1) extra memory (not including the input array).

        Args:
            seq (MutableSequence[CT]): mutable sequence

        >>> seq = [9, 4, 5, 1, 0, 3, 6]
        >>> sort_cls = InsertionSort()
        >>> sort_cls.sort(seq)
        >>> sort_cls.is_sorted(seq)
        True
        >>> sort_cls.show(seq)
        0 1 3 4 5 6 9
        """
        length = len(seq)
        for i in range(1, length):
            j = i
            while j and seq[j] < seq[j - 1]:
                self.exch(seq, j, j - 1)
                j -= 1


# 2.1.24 practice
class InsertionSortSentinel(BaseSort):

    """Insertion sort with sentinel
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Insertion sort with sentinel and half exchange version.

        Args:
            seq (MutableSequence[CT]): mutable sequence

        >>> seq = [9, 4, 5, 1, 0, 3, 6]
        >>> sort_cls = InsertionSortSentinel()
        >>> sort_cls.sort(seq)
        >>> sort_cls.is_sorted(seq)
        True
        >>> sort_cls.show(seq)
        0 1 3 4 5 6 9
        """
        exchanges = 0
        length = len(seq) - 1
        for i in range(length - 1, 0, -1):
            if seq[i] < seq[i - 1]:
                self.exch(seq, i, i - 1)
                exchanges += 1
        # seq sorted, return
        if exchanges == 0:
            return
        # 2.1.25 practice, half exchange
        for i in range(2, len(seq)):
            val = seq[i]
            j = i
            while val < seq[j - 1]:
                seq[j] = seq[j - 1]
                j -= 1
            seq[j] = val


class ShellSort(BaseSort):

    """Shell sort implementation
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Shell sort, exchange the j element
        and j-h element util i element is larger than i-1 element.
        the algorithms performance is depend on h

        Args:
            seq (MutableSequence[CT]): mutable sequence

        >>> seq = [9, 4, 5, 1, 0, 3, 6]
        >>> sort_cls = ShellSort()
        >>> sort_cls.sort(seq)
        >>> sort_cls.sort(seq)
        >>> sort_cls.is_sorted(seq)
        True
        >>> sort_cls.show(seq)
        0 1 3 4 5 6 9
        >>> sort_cls.check(seq)
        False
        >>> sort_cls.check([0, 3, 1, 7, 5])
        True
        """
        length = len(seq)
        h = 1

        while h < length / 3:
            h = 3 * h + 1

        while h >= 1:
            for i in range(h, length):
                j = i
                while j >= h and seq[j] < seq[j - h]:
                    seq[j], seq[j - h] = seq[j - h], seq[j]
                    j -= h
            h //= 3


if __name__ == '__main__':
    doctest.testmod()
