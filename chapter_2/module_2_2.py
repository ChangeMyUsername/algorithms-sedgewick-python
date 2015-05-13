#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random


class MergeSort(object):

    '''
    top-bottom merge sort implementation, merge the two sub arrays
    of the whole list and make the list partial ordered,
    and the recursion process make sure the whole list is ordered.
    for a N-size array, top-bottom merge sort need 1/2NlgN to NlgN comparisons,
    and need to access array 6NlgN times at most.
    >>> ms = MergeSort()
    >>> lst = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1, 11, 13, 31, 24]
    >>> ms.sort(lst)
    >>> lst
    [-1, 0, 1, 2, 3, 4, 5, 7, 7, 8, 9, 11, 13, 24, 31]
    '''
    def merge(self, aux, lst, low, mid, high):
        left, right = low, mid + 1

        # for i in range(low, high + 1):
        #     aux[i] = lst[i]

        for j in range(low, high + 1):
            if left > mid:
                lst[j] = aux[right]
                right += 1
            elif right > high:
                lst[j] = aux[left]
                left += 1
            elif aux[left] < aux[right]:
                lst[j] = aux[left]
                left += 1
            else:
                lst[j] = aux[right]
                right += 1

    # 2.2.11 practice, sort the small sub array with insertion sort
    def insertion_sort(self, lst, low, high):
        for i in range(low + 1, high + 1):
            j = i
            while j > low and lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
                j -= 1

    def sort(self, lst):
        # 2.2.9 practice, make aux as a function parameter.
        aux = lst[:]
        self.__sort(aux, lst, 0, len(lst) - 1)

    def __sort(self, aux, lst, low, high):
        if high <= low:
            return
        if high - low <= 7:
            self.insertion_sort(lst, low, high)
            return
        mid = (low + high) / 2
        self.__sort(lst, aux, low, mid)
        self.__sort(lst, aux, mid + 1, high)
        # 2.2.11 practice, if assistance array aux[mid] < aux[mid+1], copy the value into the origin list.
        if aux[mid] < aux[mid + 1]:
            lst[low:high - low + 1] = aux[low:high - low + 1]
        self.merge(aux, lst, low, mid, high)


class MergeSortBU(object):
    '''
    bottom-up merge sort algorithm implementation, cut the whole N-size array into
    N/sz small arrays, then merge each two of them,
    the sz parameter will be twice after merge all the subarrays,
    util the sz parameter is larger than N.

    >>> ms = MergeSortBU()
    >>> lst = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1]
    >>> ms.sort(lst)
    >>> lst
    [-1, 0, 1, 2, 3, 4, 5, 7, 7, 8, 9]
    '''
    def sort(self, lst):
        length = len(lst)
        aux = [None] * length
        size = 1
        while size < length:
            for i in range(0, length - size, size * 2):
                self.merge(aux, lst, i, i + size - 1, min(i + size * 2 - 1, length - 1))
            size *= 2

    def merge(self, aux, lst, low, mid, high):
        left, right = low, mid + 1
        for i in range(low, high + 1):
            aux[i] = lst[i]

        for j in range(low, high + 1):
            if left > mid:
                lst[j] = aux[right]
                right += 1
            elif right > high:
                lst[j] = aux[left]
                left += 1
            elif aux[left] < aux[right]:
                lst[j] = aux[left]
                left += 1
            else:
                lst[j] = aux[right]
                right += 1


# 2.2.14 practice merge two sorted list
def merge_list(lst1, lst2):
    '''
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
    '''
    assert lst1 or lst2
    if not lst1 or not lst2:
        return lst1[:] if not lst2 else lst2[:]

    i1 = i2 = 0
    new_lst = []

    for i in range(len(lst1) + len(lst2)):
        if i1 > len(lst1) - 1:
            new_lst.extend(lst2[i2:])
            break
        elif i2 > len(lst2) - 1:
            new_lst.extend(lst1[i1:])
            break
        elif lst1[i1] < lst2[i2]:
            new_lst.append(lst1[i1])
            i1 += 1
        else:
            new_lst.append(lst2[i2])
            i2 += 1
    return new_lst


# 2.2.15 practice bottom-up merge list using queue, make each element as sub queue,
# merge first two sub queue in the large queue and enqueue the result util there is only one sub queue.
def bu_merge_sort_q(lst):
    '''
    >>> bu_merge_sort_q([3, 2, 4, 7, 8, 9, 1, 0])
    [0, 1, 2, 3, 4, 7, 8, 9]
    >>> test_lst = [i for i in range(10)]
    >>> random.shuffle(test_lst)
    >>> bu_merge_sort_q(test_lst)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    '''
    for i in range(len(lst)):
        lst[i] = [lst[i]]
    while len(lst) != 1:
        lst1 = lst.pop(0)
        lst2 = lst.pop(0)
        lst.append(merge_list(lst1, lst2))
    lst.extend(lst.pop(0))
    return lst


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


# 2.2.19 practice, using merge function from merge-sort to count the reverse number
class ReverseCount(object):
    '''
    >>> rc = ReverseCount()
    >>> rc.reverse_count([1, 7, 2, 9, 6, 4, 5, 3])
    14
    '''
    def reverse_count(self, lst):
        sort_lst, aux_lst = lst[:], lst[:]
        return self.count(sort_lst, aux_lst, 0, len(lst) - 1)

    def count(self, lst, assist, low, high):
        if low >= high:
            return 0
        mid = (high + low) / 2
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
