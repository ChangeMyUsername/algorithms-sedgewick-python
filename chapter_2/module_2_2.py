#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from typing import MutableSequence

from common import CT, BaseSort


class MergeSort(BaseSort):

    """Top-bottom merge sort implementation, this algorithm divides input array
    into two halves, then call `merge` method to merge sorted two halves.

    This implementation takes ϴ(nlogn) time
    to sort any array of length n (assuming comparisons take constant time).

    This sorting algorithm is stable.
    It uses ϴ(n) extra memory (not including the input array).

    for a N-size array, top-bottom merge sort need 1/2NlgN ~ NlgN comparisons,
    and need to access array 6NlgN times at most.
    """

    def merge(self, aux: MutableSequence[CT], seq: MutableSequence[CT],
              low: int, mid: int, high: int) -> None:
        """merge method for merge sort, merge aux[low:mid] and aux[mid+1:high+1]
        into `seq`, these two sub-arrays must be sorted.

        Args:
            aux (MutableSequence[CT]): auxiliary array
            seq (MutableSequence[CT]): sorting array
            low (int): array index
            mid (int): array index
            high (int): array index
        >>> merge_sort = MergeSort()
        >>> aux_arr = [1, 5, 9, 4, 6, 11]
        >>> test_seq = [0] * 6
        >>> merge_sort.merge(aux_arr, test_seq, 0, 2, 5)
        >>> merge_sort.show(test_seq)
        1 4 5 6 9 11
        """
        # assert self.is_sorted(seq[low:mid+1])
        # assert self.is_sorted(seq[mid+1:high+1])

        left, right = low, mid + 1

        # for i in range(low, high + 1):
        #     aux[i] = lst[i]

        for j in range(low, high + 1):
            if left > mid:
                seq[j] = aux[right]
                right += 1
            elif right > high:
                seq[j] = aux[left]
                left += 1
            elif aux[left] < aux[right]:
                seq[j] = aux[left]
                left += 1
            else:
                seq[j] = aux[right]
                right += 1

    # 2.2.11 practice, apply small array with insertion sort
    def insertion_sort(
            self, seq: MutableSequence[CT], low: int, high: int) -> None:
        """Insertion sort, apply this method with certain size
        array to improve performance.

        Args:
            seq (MutableSequence[CT]): sorting array
            low (int): start index
            high (int): end index

        >>> merge_sort = MergeSort()
        >>> sequence = [0, 4, 7, 1, -3, 9]
        >>> merge_sort.insertion_sort(sequence, 0, len(sequence) - 1)
        >>> merge_sort.is_sorted(sequence)
        True
        >>> merge_sort.show(sequence)
        -3 0 1 4 7 9
        """
        for i in range(low + 1, high + 1):
            j = i
            while j > low and seq[j] < seq[j - 1]:
                self.exch(seq, j, j - 1)
                j -= 1

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Merge sort main method

        Args:
            seq (MutableSequence[CT]): sorting array

        >>> ms = MergeSort()
        >>> seq = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1, 11, 13, 31, 24]
        >>> ms.sort(seq)
        >>> ms.is_sorted(seq)
        True
        >>> ms.show(seq)
        -1 0 1 2 3 4 5 7 7 8 9 11 13 24 31
        """
        # 2.2.9 practice, make `aux` as function parameter.
        aux = seq[:]
        self.__sort(aux, seq, 0, len(seq) - 1)

    def __sort(self, aux: MutableSequence[CT], seq: MutableSequence[CT],
               low: int, high: int) -> None:

        if high <= low:
            return
        if high - low <= 7:
            self.insertion_sort(seq, low, high)
            return
        mid = int((low + high) / 2)
        self.__sort(seq, aux, low, mid)
        self.__sort(seq, aux, mid + 1, high)
        # 2.2.11 practice, if auxiliary array aux[mid] < aux[mid+1], copy
        # value to the origin list.
        if aux[mid] < aux[mid + 1]:
            seq[low:high - low + 1] = aux[low:high - low + 1]
        self.merge(aux, seq, low, mid, high)


class MergeSortBU(BaseSort):

    """
      Bottom-up merge sort algorithm implementation,
      cut the whole N-size array into
    N/sz small arrays, then merge each two of them,
    the sz parameter will be double after merge all the subarrays,
    util the sz parameter is larger than N.
    """

    def sort(self, seq: MutableSequence[CT]) -> None:
        """Merge sort main method

        Args:
            seq (MutableSequence[CT]): sorting array

        >>> ms = MergeSortBU()
        >>> seq = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1, 11, 13, 31, 24]
        >>> ms.sort(seq)
        >>> ms.is_sorted(seq)
        True
        >>> ms.show(seq)
        -1 0 1 2 3 4 5 7 7 8 9 11 13 24 31
        """
        length = len(seq)
        aux = [None] * length
        size = 1
        while size < length:
            for i in range(0, length - size, size * 2):
                self.merge(aux, seq, i, i + size - 1,
                           min(i + size * 2 - 1, length - 1))
            size *= 2

    def merge(self, aux: MutableSequence[CT], seq: MutableSequence[CT],
              low: int, mid: int, high: int) -> None:
        """Merge method for merge sort, merge aux[low:mid] and aux[mid+1:high+1]
        into `seq`, these two sub-arrays must be sorted.

        Args:
            aux (MutableSequence[CT]): auxiliary array
            seq (MutableSequence[CT]): sorting array
            low (int): array index
            mid (int): array index
            high (int): array index

        >>> merge_sort = MergeSortBU()
        >>> aux_arr = [0] * 6
        >>> test_seq = [1, 5, 9, 4, 6, 11]
        >>> merge_sort.merge(aux_arr, test_seq, 0, 2, 5)
        >>> merge_sort.show(test_seq)
        1 4 5 6 9 11
        """
        assert self.is_sorted(seq[low:mid])
        assert self.is_sorted(seq[mid+1:high])

        left, right = low, mid + 1
        for i in range(low, high + 1):
            aux[i] = seq[i]

        for j in range(low, high + 1):
            if left > mid:
                seq[j] = aux[right]
                right += 1
            elif right > high:
                seq[j] = aux[left]
                left += 1
            elif aux[left] < aux[right]:
                seq[j] = aux[left]
                left += 1
            else:
                seq[j] = aux[right]
                right += 1


# 2.2.14 practice merge two sorted list
def merge_list(seq1: MutableSequence[CT],
               seq2: MutableSequence[CT]) -> MutableSequence[CT]:
    """
    >>> merge_list([1, 2, 3, 4], [])
    [1, 2, 3, 4]
    >>> merge_list([], [1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> merge_list([1, 2, 3, 4], [4, 5, 6])
    [1, 2, 3, 4, 4, 5, 6]
    >>> merge_list([1, 2, 3, 4], [1, 2, 3, 4])
    [1, 1, 2, 2, 3, 3, 4, 4]
    >>> merge_list([1, 2], [5, 6, 7, 8])
    [1, 2, 5, 6, 7, 8]
    >>> merge_list([2, 3, 5, 9], [2, 7, 11])
    [2, 2, 3, 5, 7, 9, 11]
    """
    assert seq1 or seq2
    if not seq1 or not seq2:
        return seq1[:] if not seq2 else seq2[:]

    i1 = i2 = 0
    new_lst = []

    for i in range(len(seq1) + len(seq2)):
        if i1 > len(seq1) - 1:
            new_lst.extend(seq2[i2:])
            break
        elif i2 > len(seq2) - 1:
            new_lst.extend(seq1[i1:])
            break
        elif seq1[i1] < seq2[i2]:
            new_lst.append(seq1[i1])
            i1 += 1
        else:
            new_lst.append(seq2[i2])
            i2 += 1
    return new_lst


# 2.2.15 practice bottom-up merge list using queue,
# make each element as sub queue,
# merge first two sub queue in the large queue and enqueue the result util
# there is only one sub queue.
def bu_merge_sort_q(seq: MutableSequence[CT]) -> MutableSequence[CT]:
    """
    >>> bu_merge_sort_q([3, 2, 4, 7, 8, 9, 1, 0])
    [0, 1, 2, 3, 4, 7, 8, 9]
    >>> test_lst = [i for i in range(10)]
    >>> import random
    >>> random.shuffle(test_lst)
    >>> bu_merge_sort_q(test_lst)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    for i in range(len(seq)):
        seq[i] = [seq[i]]
    while len(seq) != 1:
        lst1 = seq.pop(0)
        lst2 = seq.pop(0)
        seq.append(merge_list(lst1, lst2))
    seq.extend(seq.pop(0))
    return seq


# 2.2.17 practice linked-list sort using merge sort
def linked_list_merge_sort(head):
    def merge(node1, node2):
        if node1 is None or node2 is None:
            return node1 or node2
        pt = res = None
        if node1.val <= node2.val:
            pt = res = node1
            node1 = node1.next_node
        else:
            pt = res = node2
            node2 = node2.next_node

        while node1 and node2:
            if node1.val < node2.val:
                pt.next_node = node1
                node1 = node1.next_node
            else:
                pt.next_node = node2
                node2 = node2.next_node
            pt = pt.next_node
        if node1:
            pt.next_node = node1
        elif node2:
            pt.next_node = node2
        return res

    if head is None or head.next is None:
        return head
    fast_pt = slow_pt = head

    while fast_pt.next_node and fast_pt.next_node.next_node:
        fast_pt = fast_pt.next_node.next_node
        slow_pt = slow_pt.next_node

    linked_list_merge_sort(head)
    linked_list_merge_sort(slow_pt)
    return merge(head, slow_pt)


# 2.2.19 practice, using merge function from merge-sort
# to count the reverse number
class ReverseCount(object):

    """
    >>> rc = ReverseCount()
    >>> rc.reverse_count([1, 7, 2, 9, 6, 4, 5, 3])
    14
    """

    def reverse_count(self, lst):
        sort_lst, aux_lst = lst[:], lst[:]
        return self.count(sort_lst, aux_lst, 0, len(lst) - 1)

    def count(self, lst, assist, low, high):
        if low >= high:
            return 0
        mid = int((high + low) / 2)
        lc = self.count(lst, assist, low, mid)
        rc = self.count(lst, assist, mid + 1, high)
        mc = self.merge_count(lst, assist, low, mid, high)
        return lc + rc + mc

    def merge_count(self, lst, assist, low, mid, high):
        assist[low:high + 1] = lst[low:high + 1]
        count, left, right = 0, low, mid + 1
        for j in range(low, high + 1):
            if left > mid:
                lst[j] = assist[right]
                right += 1
            elif right > high:
                lst[j] = assist[left]
                left += 1
            elif assist[left] < assist[right]:
                lst[j] = assist[left]
                left += 1
            else:
                lst[j] = assist[right]
                right += 1
                count += mid - left + 1
        return count


if __name__ == '__main__':
    doctest.testmod()
