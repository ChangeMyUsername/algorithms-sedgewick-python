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

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, new_children):
        self._children = new_children

    @property
    def m_size(self):
        return self._m_size

    @m_size.setter
    def m_size(self, size):
        self._m_size = size


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
        u = self._insert(self._root, key, value, self._height)
        self._size += 1
        tmp = Node(2)
        tmp.children[0] = Entry(self._root.children[0].key, None, self._root)
        tmp.children[1] = Entry(u.children[0].key, None, u)
        self._root = tmp
        self._height += 1

    def _insert(self, node, key, value, height):
        pos = 0
        new_entry = Entry(key, value, None)
        # external node
        if height == 0:
            while pos < node.m_size:
                if node[pos] and key < node[pos].key:
                    break
                pos += 1
        else:
            while pos < node.m_size:
                if pos + 1 == node.m_size or key < node.children[pos + 1].key:
                    u = self._insert(node.children[pos + 1], key, value, height - 1)
                    if not u:
                        return None
                    new_entry.key = u.children[0].key
                    new_entry.next_node = u
                    break
                pos += 1

        for i in range(node.m_size, pos, -1):
            node.children[i] = node.children[i - 1]
        node.children[pos] = new_entry
        node.m_size += 1
        if node.m_size < M_SIZE:
            return None
        return self._split(node)

    def _split(self, node):
        split_node = Node(M_SIZE / 2)
        node._m_size = M_SIZE / 2
        for i in range(M_SIZE / 2):
            split_node._children[i] = node._children[M_SIZE / 2 + i]
        return split_node

    def get(self, key):
        return self._search(self._root, key, self._height)

    def _search(self, node, key, height):
        if height == 0:
            for i in range(node.m_size):
                if node.children[i].key == key:
                    return node.children[i].value
        else:
            for i in range(node.m_size):
                if i + 1 == node.m_size or key < node.children[i + 1].key:
                    return self._search(node.children[i].next, key, height - 1)
        return None
