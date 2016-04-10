#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
M_SIZE = 6


class Entry(object):

    def __init__(self, key, value, node):
        self._key = key
        self._value = value
        self._next_node = node

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def next_node(self):
        return self._next_node


class Node(object):

    def __init__(self, k):
        self._m_size = k
        self._children = [None] * M_SIZE


class BTree(object):

    def __init__(self):
        self._root = Node(0)
        self._size = 0
        self._height = 0

    def size(self):
        return self._size

    def height(self):
        return self._height

    def put(self, key, value):
        return self._insert(self._root, key, value, self._height)

    def _insert(self, node, key, value, height):
        pos = 0
        new_entry = Entry(key, value, None)
        # external node
        if height == 0:
            while pos < node._m_size:
                if node[pos] and key < node[pos].key:
                    break
                pos += 1
        else:
            pass

    def _split(self, node):
        split_node = Node(M_SIZE / 2)
        node._m_size = M_SIZE / 2
        for i in range(M_SIZE / 2):
            split_node._children[i] = node._children[M_SIZE / 2 + i]
        return split_node

    def get(self, key):
        return self._search(self._root, key, self._height)

    def _search(self, node, key, height):
        pass
