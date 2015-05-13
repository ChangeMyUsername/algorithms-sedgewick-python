#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
import bisect


class MaxPQ(object):
    '''
    >>> mpq = MaxPQ(10)
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert_effective(i)
    ...
    >>> mpq.min_val()
    0
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_max()))
    ...
    >>> ' '.join(print_lst)
    '9 8 7 6 5 4 3 2 1 0'
    '''
    def __init__(self, size):
        self._pq = [None] * (size + 1)
        self._size = 0
        self._min = None

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def swim(self, pos):
        while pos > 1 and self._pq[pos / 2] < self._pq[pos]:
            self._pq[pos / 2], self._pq[pos] = self._pq[pos], self._pq[pos / 2]
            pos /= 2

    def sink(self, pos):
        while 2 * pos <= self._size:
            index = 2 * pos
            if index < self._size and self._pq[index] < self._pq[index + 1]:
                index += 1
            if self._pq[pos] >= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._size += 1
        self._pq[self._size] = val
        if self._min is None or self._min > val:
            self._min = val
        self.swim(self._size)

    def min_val(self):
        return self._min

    def del_max(self):
        max_val = self._pq[1]
        self._pq[1], self._pq[self._size] = self._pq[self._size], self._pq[1]
        self._pq[self._size] = None
        self._size -= 1
        self.sink(1)
        return max_val

    # 2.4.26 practice
    def swim_effective(self, pos):
        val = self._pq[pos]
        while pos > 1 and self._pq[pos / 2] < val:
            self._pq[pos] = self._pq[pos / 2]
            pos /= 2
        self._pq[pos] = val

    def insert_effective(self, val):
        self._size += 1
        self._pq[self._size] = val
        if self._min is None or self._min > val:
            self._min = val
        self.swim_effective(self._size)

    def max_val(self):
        return self._pq[1]


class MinPQ(object):
    '''
    >>> mpq = MinPQ(10)
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert(i)
    ...
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_min()))
    ...
    >>> ' '.join(print_lst)
    '0 1 2 3 4 5 6 7 8 9'
    '''
    def __init__(self, size):
        self._pq = [None] * (size + 1)
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def swim(self, pos):
        while pos > 1 and self._pq[pos / 2] > self._pq[pos]:
            self._pq[pos / 2], self._pq[pos] = self._pq[pos], self._pq[pos / 2]
            pos /= 2

    def sink(self, pos):
        while 2 * pos <= self._size:
            index = 2 * pos
            if index < self._size and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._size += 1
        self._pq[self._size] = val
        self.swim(self._size)

    def del_min(self):
        min_val = self._pq[1]
        self._pq[1], self._pq[self._size] = self._pq[self._size], self._pq[1]
        self._pq[self._size] = None
        self._size -= 1
        self.sink(1)
        return min_val

    def min_val(self):
        return self._pq[1]


# 2.4.22 practice, a little change for python version, the queue's size is not limited.
class MaxPQDynamic(object):
    '''
    >>> mpq = MaxPQDynamic()
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert(i)
    ...
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_max()))
    ...
    >>> ' '.join(print_lst)
    '9 8 7 6 5 4 3 2 1 0'
    '''
    def __init__(self):
        self._pq = []

    def is_empty(self):
        return len(self._pq) == 0

    def size(self):
        return len(self._pq)

    def swim(self, pos):
        while pos > 0 and self._pq[(pos - 1) / 2] < self._pq[pos]:
            self._pq[(pos - 1) / 2], self._pq[pos] = self._pq[pos], self._pq[(pos - 1) / 2]
            pos = (pos - 1) / 2

    def sink(self, pos):
        length = len(self._pq) - 1
        while 2 * pos + 1 <= length:
            index = 2 * pos + 1
            if index < length and self._pq[index] < self._pq[index + 1]:
                index += 1
            if self._pq[pos] >= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._pq.append(val)
        self.swim(len(self._pq) - 1)

    def del_max(self):
        max_val = self._pq[0]
        last_index = len(self._pq) - 1
        self._pq[0], self._pq[last_index] = self._pq[last_index], self._pq[0]
        self._pq.pop(last_index)
        self.sink(0)
        return max_val

    def max_val(self):
        return self._pq[0]


class MinPQDynamic(object):
    '''
    >>> mpq = MinPQDynamic()
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert(i)
    ...
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_min()))
    ...
    >>> ' '.join(print_lst)
    '0 1 2 3 4 5 6 7 8 9'
    '''
    def __init__(self):
        self._pq = []

    def is_empty(self):
        return len(self._pq) == 0

    def size(self):
        return len(self._pq)

    def swim(self, pos):
        while pos > 0 and self._pq[(pos - 1) / 2] > self._pq[pos]:
            self._pq[(pos - 1) / 2], self._pq[pos] = self._pq[pos], self._pq[(pos - 1) / 2]
            pos = (pos - 1) / 2

    def binary_swim(self, pos):
        index, vals, temp, target = [], [], pos, self._pq[pos]
        while temp:
            index.append(temp)
            vals.append(self._pq[temp])
            temp = (temp - 1) / 2

        insert_pos = bisect.bisect_left(vals, target)
        if insert_pos == len(vals):
            return

        i = insert_pos - 1
        while i < len(vals) - 1:
            self._pq[index[i + 1]] = self._pq[index[i]]
            i += 1

        self._pq[insert_pos - 1] = target

    def sink(self, pos):
        length = len(self._pq) - 1
        while 2 * pos + 1 <= length:
            index = 2 * pos + 1
            if index < length and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._pq.append(val)
        self.binary_swim(len(self._pq) - 1)

    def del_min(self):
        min_val = self._pq[0]
        last_index = len(self._pq) - 1
        self._pq[0], self._pq[last_index] = self._pq[last_index], self._pq[0]
        self._pq.pop(last_index)
        self.sink(0)
        return min_val

    def min_val(self):
        return self._pq[0]


# 2.4.30 practice
class MeanHeap(object):
    '''
    >>> mh = MeanHeap()
    >>> for i in range(9):
    ...     mh.insert(i)
    ...
    >>> mh.median()
    4
    >>> mh.insert(9)
    >>> mh.median()
    4.5
    >>> mh.insert(10)
    >>> mh.median()
    5
    '''
    def __init__(self):
        self._min_heap = MinPQDynamic()
        self._max_heap = MaxPQDynamic()

    def is_empty(self):
        return self._min_heap.is_empty() and self._max_heap.is_empty()

    def size(self):
        return self._min_heap.size() and self._max_heap.size()

    def median(self):
        if self.is_empty():
            return None
        if self._min_heap.size() < self._max_heap.size():
            return self._max_heap.max_val()

        if self._max_heap.size() < self._min_heap.size():
            return self._min_heap.min_val()

        return float(self._min_heap.min_val() + self._max_heap.max_val()) / 2

    def insert(self, val):
        if self._min_heap.is_empty():
            self._min_heap.insert(val)
            return

        if self._max_heap.is_empty():
            self._max_heap.insert(val)
            return

        if val < self._max_heap.max_val():
            if self._max_heap.size() < self._min_heap.size():
                self._max_heap.insert(val)
            else:
                self._min_heap.insert(self._max_heap.del_max())
                self._max_heap.insert(val)

        if val > self._min_heap.min_val():
            if self._min_heap.size() < self._max_heap.size():
                self._min_heap.insert(val)
            else:
                self._max_heap.insert(self._min_heap.del_min())
                self._min_heap.insert(val)

        if val > self._max_heap.max_val() and val < self._min_heap.min_val():
            if self._max_heap.size() < self._min_heap.size():
                self._max_heap.insert(val)
            else:
                self._min_heap.insert(val)


# 2.4.33 index minimum priority queue.
class IndexMinPQ(object):

    def __init__(self):
        self._pq = []
        self._qp = []
        self._keys = []

    def is_empty(self):
        return len(self._pq) == 0

    def contains(self, k):
        return k in self._qp


class Node(object):

    def __init__(self, i, j):
        self._sum = i ** 3 + j ** 3
        self.i = i
        self.j = j

    def __cmp__(self, other):
        if self._sum < other._sum:
            return -1
        elif self._sum > other._sum:
            return 1
        return 0

    def __str__(self):
        return '{} = {}^3 + {}^3'.format(self._sum, self.i, self.j)


# 2.4.25 practice, cube sum implementation.
def cubesum():
    min_pq = MinPQDynamic()
    n = 10 ** 6
    for i in range(n):
        min_pq.insert(Node(i, i))

    while not min_pq.is_empty():
        node = min_pq.del_min()
        print(node)
        if node.j < n:
            min_pq.insert(Node(node.i, node.j + 1))


def heap_sort(lst):
    '''
    heap-sort implementation, using priority queue sink() method as util function,
    first build the maximum priority queue, and exchange list[0] and lst[size], then size minus one,
    and sink the list[0] again, util size equals zero.

    >>> lst = []
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> heap_sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    '''
    def sink(lst, pos, size):
        while 2 * pos + 1 <= size:
            index = 2 * pos + 1
            if index < size and lst[index + 1] > lst[index]:
                index += 1
            if lst[pos] >= lst[index]:
                break
            lst[pos], lst[index] = lst[index], lst[pos]
            pos = index

    size = len(lst) - 1
    for i in range(size / 2, -1, -1):
        sink(lst, i, size)

    while size:
        lst[0], lst[size] = lst[size], lst[0]
        size -= 1
        sink(lst, 0, size)


if __name__ == '__main__':
    doctest.testmod()
    # cubesum()
