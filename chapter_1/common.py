#!/usr/bin/env python
# -*- encoding:UTF-8 -*-


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


class DoubleNode(object):

    def __init__(self, val):
        self._val = val
        self._prev = self._next = None

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, node):
        self._prev = node

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value
