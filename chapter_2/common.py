#!/usr/bin/env python
# -*- encoding:UTF-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar, MutableSequence


class Comparable(metaclass=ABCMeta):
    """Comparable class for type hint
    """
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """To get current element is less than `other` or not.

        Args:
            other (Any): other element to compare,
                         type of `other` must match current element

        Returns:
            bool: True if current element < `other` else False
        """
        pass


CT = TypeVar('CT', bound=Comparable)


class BaseSort(metaclass=ABCMeta):
    """Sorting algorithms base class
    """

    @abstractmethod
    def sort(self, seq: MutableSequence[CT]) -> None:
        pass

    # 2.1.16 practice
    def check(self, seq: MutableSequence[CT]) -> bool:
        pre_sort_fp = ''.join(map(str, seq))
        self.sort(seq)
        after_sort_fp = ''.join(map(str, seq))
        if pre_sort_fp != after_sort_fp:
            return True
        return False

    def exch(self, seq: MutableSequence[CT], index1: int, index2: int) -> None:
        """Exchange two elements in `seq`.

        Args:
            seq (MutableSequence[CT]): mutable sequence
            index1 (int): element index
            index2 (int): other element index
        """
        seq[index1], seq[index2] = seq[index2], seq[index1]

    def show(self, seq: MutableSequence[CT]) -> None:
        """Print `seq` all elements.

        Args:
            seq (MutableSequence[CT]): mutable sequence
        """
        print(' '.join(map(str, seq)))

    def is_sorted(self, seq: MutableSequence[CT]) -> bool:
        """Check if `seq` is sorted.

        Args:
            seq (MutableSequence[CT]): mutable sequence

        Returns:
            bool: True if `seq` is sorted else False
        """
        for i in range(1, len(seq)):
            if seq[i] < seq[i - 1]:
                return False
        return True
