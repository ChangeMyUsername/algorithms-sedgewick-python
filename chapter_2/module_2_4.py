#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import annotations

import bisect
import doctest
import sys
from collections import deque
from typing import MutableSequence

from common import CT

MIN_VAL = -sys.maxsize - 1
MAX_VAL = sys.maxsize


class MaxPQ(object):

    """Max piority queue implementation.
    """

    def __init__(self, size: int) -> None:
        """Max priority queue initialization.

        Args:
            size (int): priority queue size
        """
        self._pq = [MIN_VAL] * (size + 1)
        self._size = 0
        self._min = None

    def is_empty(self) -> bool:
        """Check if queue is empty or not.

        Returns:
            bool: True if queue is empty else False
        """
        return self._size == 0

    def size(self) -> int:
        """Return the size of queue.

        Returns:
            int: size of queue
        """
        return self._size

    def exch(self, index1: int, index2: int) -> None:
        """Change queue element's position.

        Args:
            pq (MutableSequence[CT]): priority queue
            index1 (int): element index
            index2 (int): element index
        """
        self._pq[index1], self._pq[index2] = self._pq[index2], self._pq[index1]

    def swim(self, pos: int) -> None:
        """Restore queue's order by moving up current element until
        parent element's priority is higher than current element.

        Args:
            pos (int): current element index
        """
        while pos > 1 and self._pq[pos // 2] < self._pq[pos]:
            self.exch(pos, pos // 2)
            pos //= 2

    def sink(self, pos: int) -> None:
        """Restore queue's order by sinking current element until
        children elements priority are lower than current element.

        Args:
            pos (int): current element index
        """
        while 2 * pos <= self._size:
            index = 2 * pos
            if index < self._size and self._pq[index] < self._pq[index + 1]:
                index += 1
            if self._pq[pos] >= self._pq[index]:
                break
            self.exch(index, pos)
            pos = index

    def insert(self, val: CT) -> None:
        """Insert element into piority queue, append `val` to priority queue,
        then call `swim` method to restore piority queue's order.

        Args:
            val (CT): element to insert

        >>> mpq = MaxPQ(10)
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> mpq.size()
        10
        >>> mpq.is_empty()
        False
        >>> mpq.max_val()
        9
        >>> mpq.min_val()
        0
        """
        self._size += 1
        self._pq[self._size] = val
        if self._min is None or self._min > val:
            self._min = val
        self.swim(self._size)

    # 2.4.27 practice
    def min_val(self) -> CT:
        """Return minimum value in piority queue.

        Returns:
            CT: maximum value in priority queue
        """
        return self._min

    def del_max(self) -> CT:
        """Remove maximum value and returns, exchange maximum element's position
        and last element position, then set last element position as `None`.
        After that call `sink` method to restore priority queue's order.

        Returns:
            CT: removed element

        >>> mpq = MaxPQ(10)
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> [mpq.del_max() for _ in range(10)]
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        >>> mpq.is_empty()
        True
        >>> mpq.size()
        0
        >>> mpq.insert(1)
        """
        max_val = self._pq[1]
        self.exch(1, self._size)
        self._pq[self._size] = MIN_VAL
        self._size -= 1
        self.sink(1)
        return max_val

    # 2.4.26 practice
    def swim_effective(self, pos: int) -> None:
        """Use insertion sort approach to reduce element exchange operations.

        Args:
            pos (int): element index
        """
        val = self._pq[pos]
        while pos > 1 and self._pq[pos // 2] < val:
            self._pq[pos] = self._pq[pos // 2]
            pos //= 2
        self._pq[pos] = val

    def insert_effective(self, val: CT) -> None:
        """Insert operation with calling `swim_effective` method.

        Args:
            val (CT): element to insert

        >>> mpq = MaxPQ(10)
        >>> lst = [i for i in range(10)]
        >>> import random
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
        """
        self._size += 1
        self._pq[self._size] = val
        if self._min is None or self._min > val:
            self._min = val
        self.swim_effective(self._size)

    def max_val(self) -> CT:
        """Return maximum value in piority queue.

        Returns:
            CT: maximum value in priority queue
        """
        return self._pq[1]


class MinPQ(object):

    """Min priority quque implementation.
    >>> mpq = MinPQ(10)
    >>> lst = [i for i in range(10)]
    >>> import random
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
    """

    def __init__(self, size: int) -> None:
        """Initialization method.

        Args:
            size (int): priority queue size
        """
        self._pq = [MAX_VAL] * (size + 1)
        self._size = 0

    def is_empty(self) -> bool:
        """Check if queue is empty or not.

        Returns:
            bool: True if queue is empty else False
        """
        return self._size == 0

    def size(self) -> int:
        """Return the size of queue.

        Returns:
            int: size of queue
        """
        return self._size

    def exch(self, index1: int, index2: int) -> None:
        """Change queue element's position.

        Args:
            pq (MutableSequence[CT]): priority queue
            index1 (int): element index
            index2 (int): element index
        """
        self._pq[index1], self._pq[index2] = self._pq[index2], self._pq[index1]

    def swim(self, pos: int) -> None:
        """Restore queue's order by moving up current element until
        parent element's priority is lower than current element.

        Args:
            pos (int): current element index
        """
        while pos > 1 and self._pq[int(pos / 2)] > self._pq[pos]:
            self.exch(int(pos / 2), pos)
            pos //= 2

    def sink(self, pos: int) -> None:
        """Restore queue's order by sinking current element until
        children elements priority are higher than current element.

        Args:
            pos (int): current element index
        """
        while 2 * pos <= self._size:
            index = 2 * pos
            if index < self._size and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self.exch(index, pos)
            pos = index

    def insert(self, val: CT) -> None:
        """Insert element into piority queue, append `val` to priority queue,
        then call `swim` method to restore piority queue's order.

        Args:
            val (CT): element to insert

        >>> mpq = MinPQ(10)
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> mpq.size()
        10
        >>> mpq.is_empty()
        False
        >>> mpq.min_val()
        0
        """
        self._size += 1
        self._pq[self._size] = val
        self.swim(self._size)

    def del_min(self) -> CT:
        """Remove minimum value and returns, exchange minimum element's position
        and last element position, then set last element position as `None`.
        After that call `sink` method to restore priority queue's order.

        Returns:
            CT: removed element

        >>> mpq = MinPQ(10)
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> [mpq.del_min() for _ in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> mpq.is_empty()
        True
        >>> mpq.size()
        0
        >>> mpq.insert(1)
        """
        min_val = self._pq[1]
        self._pq[1], self._pq[self._size] = self._pq[self._size], self._pq[1]
        self._pq[self._size] = MAX_VAL
        self._size -= 1
        self.sink(1)
        return min_val

    def min_val(self) -> CT:
        """Return minimum value in piority queue.

        Returns:
            CT: minimum value in priority queue
        """
        return self._pq[1]


def heap_sort(seq: MutableSequence[CT]) -> None:
    """Heap-sort implementation, iterate through sequence and call `sink` function
    to let every element moving to proper position.

    Args:
        seq (MutableSequence[CT]): input sequence

    >>> seq = [i for i in range(10)]
    >>> import random
    >>> random.shuffle(seq)
    >>> heap_sort(seq)
    >>> seq
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """

    def sink(seq: MutableSequence[CT], pos: int, size: int) -> None:
        while 2 * pos + 1 <= size:
            index = 2 * pos + 1
            if index < size and seq[index + 1] > seq[index]:
                index += 1
            if seq[pos] >= seq[index]:
                break
            seq[pos], seq[index] = seq[index], seq[pos]
            pos = index

    size = len(seq) - 1
    for i in range(size // 2, -1, -1):
        sink(seq, i, size)

    while size:
        seq[0], seq[size] = seq[size], seq[0]
        size -= 1
        sink(seq, 0, size)


# 2.4.15 practice
def is_min_heapified(seq: MutableSequence[CT]) -> bool:
    """Check if `seq` is min-heapified.

    Args:
        seq (MutableSequence[CT]): [description]

    Returns:
        bool: [description]

    >>> import heapq
    >>> import random
    >>> seq = [i for i in range(4)]
    >>> random.shuffle(seq)
    >>> heapq.heapify(seq)
    >>> is_min_heapified(seq)
    True
    >>> seq = [i for i in range(5)]
    >>> random.shuffle(seq)
    >>> heapq.heapify(seq)
    >>> is_min_heapified(seq)
    True
    >>> seq = [i for i in range(7)]
    >>> seq.insert(0, 9)
    >>> is_min_heapified(seq)
    False
    >>> random.shuffle(seq)
    >>> heapq.heapify(seq)
    >>> is_min_heapified(seq)
    True
    """
    queue = deque()
    queue.append(0)
    while len(queue) > 0:
        pos = queue.popleft()
        left_child = seq[pos * 2 + 1] if pos * 2 + 1 < len(seq) else None
        right_child = seq[pos * 2 + 2] if pos * 2 + 2 < len(seq) else None
        if ((left_child is not None and seq[pos] > left_child) or
                (right_child is not None and seq[pos] > right_child)):
            return False
        if pos * 2 + 1 < len(seq):
            queue.append(pos * 2 + 1)
        if pos * 2 + 2 < len(seq):
            queue.append(pos * 2 + 2)
    return True


# 2.4.22 practice, a little change for python version,
# queue's size is not limited.
class MaxPQDynamic(object):

    """Max priority queue without length limitation.
    """

    def __init__(self) -> None:
        """Initialize method
        """
        self._pq = []

    def is_empty(self) -> bool:
        """Check if queue is empty or not.

        Returns:
            bool: True if queue is empty else False
        """
        return len(self._pq) == 0

    def size(self) -> int:
        """Return the size of queue.

        Returns:
            int: size of queue
        """
        return len(self._pq)

    def exch(self, index1: int, index2: int) -> None:
        """Change queue element's position.

        Args:
            pq (MutableSequence[CT]): priority queue
            index1 (int): element index
            index2 (int): element index
        """
        self._pq[index1], self._pq[index2] = self._pq[index2], self._pq[index1]

    def swim(self, pos: int) -> None:
        """Restore queue's order by moving up current element until
        parent element's priority is higer than current element.

        Args:
            pos (int): current element index
        """
        while pos > 0 and self._pq[(pos - 1) // 2] < self._pq[pos]:
            self.exch((pos - 1) // 2, pos)
            pos = (pos - 1) // 2

    def sink(self, pos: int) -> None:
        """Restore queue's order by sinking current element until
        children elements priority are lower than current element.

        Args:
            pos (int): current element index
        """
        length = len(self._pq) - 1
        while 2 * pos + 1 <= length:
            index = 2 * pos + 1
            if index < length and self._pq[index] < self._pq[index + 1]:
                index += 1
            if self._pq[pos] >= self._pq[index]:
                break
            self.exch(index, pos)
            pos = index

    def insert(self, val: CT) -> None:
        """Insert element into piority queue, append `val` to priority queue,
        then call `swim` method to restore piority queue's order.

        Args:
            val (CT): element to insert

        >>> mpq = MaxPQDynamic()
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> mpq.size()
        10
        >>> mpq.is_empty()
        False
        >>> mpq.max_val()
        9
        """
        self._pq.append(val)
        self.swim(len(self._pq) - 1)

    def del_max(self) -> CT:
        """Remove maximum value and returns, exchange maximum element's position
        and last element position, then set last element position as `None`.
        After that call `sink` method to restore priority queue's order.

        Returns:
            CT: removed element

        >>> mpq = MaxPQDynamic()
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> [mpq.del_max() for _ in range(10)]
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        >>> mpq.is_empty()
        True
        >>> mpq.size()
        0
        >>> mpq.insert(1)
        """
        max_val = self._pq[0]
        last_index = len(self._pq) - 1
        self._pq[0], self._pq[last_index] = self._pq[last_index], self._pq[0]
        self._pq.pop(last_index)
        self.sink(0)
        return max_val

    def max_val(self) -> CT:
        """Return maximum value in piority queue.

        Returns:
            CT: maximum value in priority queue
        """
        return self._pq[0]


class MinPQDynamic(object):

    """Max priority queue without length limitation.
    """

    def __init__(self) -> None:
        """Initialize method
        """
        self._pq = []

    def is_empty(self) -> bool:
        """Check if queue is empty or not.

        Returns:
            bool: True if queue is empty else False
        """
        return len(self._pq) == 0

    def size(self) -> int:
        """Return the size of queue.

        Returns:
            int: size of queue
        """
        return len(self._pq)

    def exch(self, index1: int, index2: int) -> None:
        """Change queue element's position.

        Args:
            pq (MutableSequence[CT]): priority queue
            index1 (int): element index
            index2 (int): element index
        """
        self._pq[index1], self._pq[index2] = self._pq[index2], self._pq[index1]

    def swim(self, pos: int) -> None:
        """Restore queue's order by moving up current element until
        parent element's priority is lower than current element.

        Args:
            pos (int): current element index
        """
        while pos > 0 and self._pq[(pos - 1) // 2] > self._pq[pos]:
            self.exch((pos - 1) // 2, pos)
            pos = (pos - 1) // 2

    def binary_swim(self, pos: int) -> None:
        index, vals, temp, target = [], [], pos, self._pq[pos]
        while temp:
            index.append(temp)
            vals.append(self._pq[temp])
            temp = (temp - 1) // 2

        insert_pos = bisect.bisect_left(vals, target)
        if insert_pos == len(vals):
            return

        i = insert_pos - 1
        while i < len(vals) - 1:
            self._pq[index[i + 1]] = self._pq[index[i]]
            i += 1

        self._pq[insert_pos - 1] = target

    def sink(self, pos):
        """Restore queue's order by sinking current element until
        children elements priority are higher than current element.

        Args:
            pos (int): current element index
        """
        length = len(self._pq) - 1
        while 2 * pos + 1 <= length:
            index = 2 * pos + 1
            if index < length and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self.exch(index, pos)
            pos = index

    def insert(self, val: CT) -> None:
        """Insert element into piority queue, append `val` to priority queue,
        then call `swim` method to restore piority queue's order.

        Args:
            val (CT): element to insert

        >>> mpq = MinPQDynamic()
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> mpq.size()
        10
        >>> mpq.is_empty()
        False
        >>> mpq.min_val()
        0
        """
        self._pq.append(val)
        self.swim(len(self._pq) - 1)

    def del_min(self) -> CT:
        """Remove minimum value and returns, exchange minimum element's position
        and last element position, then set last element position as `None`.
        After that call `sink` method to restore priority queue's order.

        Returns:
            CT: removed element

        >>> mpq = MinPQDynamic()
        >>> seq = [i for i in range(10)]
        >>> import random
        >>> random.shuffle(seq)
        >>> for i in seq:
        ...     mpq.insert(i)
        ...
        >>> [mpq.del_min() for _ in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> mpq.is_empty()
        True
        >>> mpq.size()
        0
        >>> mpq.insert(1)
        """
        min_val = self._pq[0]
        last_index = len(self._pq) - 1
        self._pq[0], self._pq[last_index] = self._pq[last_index], self._pq[0]
        self._pq.pop(last_index)
        self.sink(0)
        return min_val

    def min_val(self) -> CT:
        """Return minimum value in piority queue.

        Returns:
            CT: minimum value in priority queue
        """
        return self._pq[0]


# 2.4.30 practice
class MeanHeap(object):

    """Median heap implementation, it creates two heaps,
    max heap contains half of lower sets of all elements, and
    min heap contains half of higher set of all elements.
    """

    def __init__(self) -> None:
        """Initialize method, initialize min heap and max heap.
        """
        self._min_heap = MinPQDynamic()
        self._max_heap = MaxPQDynamic()

    def is_empty(self) -> bool:
        """Check if mean heap is empty or not.

        Returns:
            bool: True if mean heap is empty else False
        """
        return self._min_heap.is_empty() and self._max_heap.is_empty()

    def size(self) -> int:
        """Return the size of mean heap

        Returns:
            int: size of mean heap
        """
        return self._min_heap.size() and self._max_heap.size()

    def median(self) -> CT:
        """Return median value of mean heap, if one of these heaps
        contains more elements than other, then return min(max) element
        from that heap.

        If both heaps have the same size, then return avarage value.

        Returns:
            CT: median value
        """
        if self.is_empty():
            return None
        if self._min_heap.size() < self._max_heap.size():
            return self._max_heap.max_val()

        if self._max_heap.size() < self._min_heap.size():
            return self._min_heap.min_val()

        return (self._min_heap.min_val() + self._max_heap.max_val()) / 2

    def insert(self, val: CT) -> None:
        """Mean heap insert operation, first need to compare `val` to
        minimum value in min heap and maximum value in max heap, then
        insert into min(max) heap based on comparison result and heap size.

        Args:
            val (CT): element to insert

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
        """
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
        if node.j < n:
            min_pq.insert(Node(node.i, node.j + 1))


if __name__ == '__main__':
    doctest.testmod()
    # cubesum()
