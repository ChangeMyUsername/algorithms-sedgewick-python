#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import print_function
import doctest
from common import Node


class LinkedList(object):
    '''
    linked list practice.
    >>> ######### init linked list test case.
    >>> lst = LinkedList()
    >>> for i in range(1, 5):
    ...     lst.append(i)
    ...
    >>> lst.print_list()
    1 2 3 4
    >>> ######## test delete_last() function, remove all nodes from linked list.
    >>> while lst.size():
    ...     lst.delete_last()
    ...
    >>> lst.print_list()
    >>> ######## re-init linked list.
    >>> lst = LinkedList()
    >>> for i in range(1, 5):
    ...     lst.append(i)
    ...
    >>> ######## test find() function.
    >>> lst.find(5)
    False
    >>> lst.find(4)
    True
    >>> lst.find(1)
    True
    >>> ######### test delete() function.
    >>> lst.delete(1)
    >>> lst.print_list()
    2 3 4
    >>> lst.delete(4)
    >>> lst.print_list()
    2 3 4
    >>> lst.delete(2)
    >>> lst.print_list()
    2 4
    >>> ######## new test list.
    >>> lst2 = LinkedList()
    >>> for i in range(10):
    ...     lst2.append(i)
    ...
    >>> ######## test remove_after function.
    >>> lst2.remove_after(8)
    >>> lst2.remove_after(0)
    >>> lst2.print_list()
    0 2 3 4 5 6 7 8
    >>> ####### test insert_after function.
    >>> lst2.insert_after(0, 1)
    >>> lst2.print_list()
    0 1 2 3 4 5 6 7 8
    >>> lst2.insert_after(8, 9)
    >>> lst2.print_list()
    0 1 2 3 4 5 6 7 8 9
    >>> ###### test max_value function.
    >>> lst2.max_value()
    9
    >>> ##### test remove function, cannot delete all-same-value list yet.
    >>> lst2.append(8)
    >>> lst2.append(1)
    >>> lst2.remove(1)
    >>> lst2.remove(8)
    >>> lst2.print_list()
    0 2 3 4 5 6 7 9
    >>> lst3 = LinkedList()
    >>> for i in range(5):
    ...     lst3.append(3)
    ...
    >>> lst3.remove(3)
    >>> lst3.remove(3)
    >>> lst3.print_list()
    >>>
    >>> for i in range(1, 10):
    ...      lst3.append(i)
    ...
    >>> node = lst3.reverse()
    >>> while node:
    ...    print(node.val, end=' ')
    ...    node = node.next_node
    ...
    9 8 7 6 5 4 3 2 1 
    '''
    def __init__(self):
        self._first = None
        self._size = 0

    def print_list(self):
        tmp = self._first
        while tmp:
            if not tmp.next_node:
                print(tmp.val)
            else:
                print(tmp.val, end=' ')
            tmp = tmp.next_node

    def append(self, val):
        if not self._first:
            self._first = Node(val)
            self._size += 1
            return
        tmp = self._first
        while tmp.next_node:
            tmp = tmp.next_node
        tmp.next_node = Node(val)
        self._size += 1

    # 1.3.19 practice
    def delete_last(self):
        tmp = self._first
        if not tmp:
            return
        if not self._first.next_node:
            self._first = None
            self._size -= 1
            return
        while tmp.next_node.next_node:
            tmp = tmp.next_node
        tmp.next_node = None
        self._size -= 1

    # 1.3.21 practice
    def find(self, val):
        tmp = self._first
        while tmp:
            if tmp.val == val:
                return True
            tmp = tmp.next_node
        return False

    def size(self):
        return self._size

    # 1.3.20 practice
    def delete(self, pos):
        if pos > self._size:
            return
        if pos == 1:
            self._first = self._first.next_node
            self._size -= 1
            return
        tmp, count = self._first, 1
        while count != pos - 1:
            count += 1
            tmp = tmp.next_node
        target = tmp.next_node
        tmp.next_node = tmp.next_node.next_node
        target.next_node = None
        self._size -= 1

    # 1.3.24 practice, accept val as parameter instead of node as parameter
    def remove_after(self, item):
        tmp = self._first
        while tmp.next_node:
            if tmp.val == item:
                tmp.next_node = tmp.next_node.next_node
                break
                self._size -= 1
            tmp = tmp.next_node

    # 1.3.25 practice, accept val as parameter instead of node as parameter
    def insert_after(self, current_node_item, new_node_item):
        tmp = self._first
        while tmp:
            if tmp.val == current_node_item:
                old_next_node = tmp.next_node
                new_node = Node(new_node_item)
                tmp.next_node = new_node
                new_node.next_node = old_next_node
                self._size += 1
                break
            tmp = tmp.next_node

    # 1.3.26 practice
    def remove(self, key):
        if not self._first.next_node and self._first.val == key:
            self._first = None
            self._size = 0
            return

        tmp = self._first
        prev = None
        while tmp:
            if tmp.val == key:
                if not prev:
                    target = tmp
                    tmp = tmp.next_node
                    target.next_node = None
                else:
                    prev.next_node = tmp.next_node
                self._size -= 1
            prev = tmp
            tmp = tmp.next_node

    # 1.3.27 practice
    def max_value(self):
        tmp = self._first
        max_val = None
        while tmp:
            if max_val is None:
                max_val = tmp.val
            if tmp.val > max_val:
                max_val = tmp.val
            tmp = tmp.next_node
        return max_val

    # 1.3.30 practice
    def reverse(self):
        first = self._first
        reverse_node = None
        while first:
            second = first.next_node
            first.next_node = reverse_node
            reverse_node = first
            first = second
        return reverse_node


if __name__ == '__main__':
    doctest.testmod()
