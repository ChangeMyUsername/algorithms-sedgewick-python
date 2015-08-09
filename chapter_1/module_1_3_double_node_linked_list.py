#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import print_function
from common import DoubleNode
import doctest


# 1.3.31 practice
class LinkedList(object):

    '''
    the double-node linked list implementation which the node has prev and next attribute.
    >>> lst = LinkedList()
    >>> lst.push_back(1)
    >>> lst.push_front(2)
    >>> for i in lst:
    ...     print(i)
    ...
    2
    1
    >>> lst.size()
    2
    >>> lst.is_empty()
    False
    >>> lst.pop_front()
    2
    >>> lst.pop_front()
    1
    >>> lst.is_empty()
    True
    >>> lst.pop_front()
    >>> lst.push_back(1)
    >>> lst.push_back(2)
    >>> lst.pop_back()
    2
    >>> lst.pop_back()
    1
    >>> lst.pop_back()
    >>>
    >>> lst.is_empty()
    True
    >>> lst.push_back(1)
    >>> lst.insert_after(1, DoubleNode(2))
    >>> lst.insert_before(2, DoubleNode(3))
    >>> for i in lst:
    ...     print(i)
    ...
    1
    3
    2
    >>> for i in range(10):
    ...     lst.push_back(i)
    ...
    >>> lst.remove(1)
    >>> lst.remove(3)
    >>> [i for i in lst]
    [2, 0, 2, 4, 5, 6, 7, 8, 9]
    >>> lst.remove(2)
    >>> [i for i in lst]
    [0, 4, 5, 6, 7, 8, 9]
    '''

    def __init__(self):
        self._first = self._last = None
        self._size = 0

    def __iter__(self):
        tmp = self._first
        while tmp:
            yield tmp.val
            tmp = tmp.next

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push_front(self, item):
        old = self._first
        self._first = DoubleNode(item)
        self._first.next = old
        if old:
            old.prev = self._first
        else:
            self._last = self._first
        self._size += 1

    def push_back(self, item):
        old = self._last
        self._last = DoubleNode(item)
        self._last.prev = old
        if old:
            old.next = self._last
        else:
            self._first = self._last
        self._size += 1

    def pop_front(self):
        if self._first:
            old = self._first
            self._first = self._first.next
            old.next = None
            if self._first:
                self._first.prev = None
            else:
                self._last = None
            self._size -= 1
            return old.val
        return None

    def pop_back(self):
        if self._last:
            old = self._last
            self._last = self._last.prev
            old.prev = None
            if self._last:
                self._last.next = None
            else:
                self._first = None
            self._size -= 1
            return old.val
        return None

    def insert_before(self, target_value, new_node):
        tmp = self._first
        while tmp and tmp.val != target_value:
            tmp = tmp.next

        if not tmp:
            return

        if not tmp.prev:
            tmp.prev = new_node
            new_node.next = tmp
            self._first = new_node
            self._size += 1
            return

        prev_node = tmp.prev
        prev_node.next = new_node
        new_node.prev = prev_node

        tmp.prev = new_node
        new_node.next = tmp

        self._size += 1

    def insert_after(self, target_value, new_node):
        tmp = self._first
        while tmp and tmp.val != target_value:
            tmp = tmp.next

        if not tmp:
            return

        if not tmp.next:
            tmp.next = new_node
            new_node.prev = tmp
            self._last = new_node
            self._size += 1
            return

        next_node = tmp.next
        next_node.prev = new_node
        new_node.next = next_node

        tmp.next = new_node
        new_node.prev = tmp

        self._size += 1

    def remove(self, item):
        if not self._first.next and self._first.val == item:
            self._first = None
            self._size = 0
            return

        tmp = self._first
        while tmp:
            flag = False
            if tmp.val == item:
                flag = True
                if not tmp.prev:
                    target = tmp
                    tmp = tmp.next
                    tmp.prev = target.next = None
                    self._first = tmp
                else:
                    prev_node, next_node = tmp.prev, tmp.next
                    tmp.prev = tmp.next = None
                    prev_node.next, next_node.prev = next_node, prev_node
                    tmp = next_node
                self._size -= 1
            if not flag:
                tmp = tmp.next

if __name__ == '__main__':
    doctest.testmod()
