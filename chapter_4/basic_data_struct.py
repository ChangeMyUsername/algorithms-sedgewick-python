#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
"""
    copy from module_1_3.py, this is for avoiding package import problems.
"""


class Node(object):

    def __init__(self, val):
        self._val = val
        self.next_node = None

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, node):
        self._next_node = node


class Stack(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self):
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    # 1.3.7 practice
    def peek(self):
        if self._first:
            return self._first.val
        return None


class Queue(object):

    def __init__(self, q=None):
        self._first = None
        self._last = None
        self._size = 0
        if q:
            for item in q:
                self.enqueue(item)

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def enqueue(self, val):
        old_last = self._last
        self._last = Node(val)
        self._last.next_node = None
        if self.is_empty():
            self._first = self._last
        else:
            old_last.next_node = self._last
        self._size += 1

    def dequeue(self):
        if not self.is_empty():
            val = self._first.val
            self._first = self._first.next_node
            if self.is_empty():
                self._last = None
            self._size -= 1
            return val
        return None


class Bag(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def add(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size
