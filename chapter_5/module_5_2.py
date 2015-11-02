#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


R = 256


class Node(object):

    def __init__(self):
        self._val = None
        self.next_nodes = [None] * 256

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value


class Trie(object):

    def __init__(self):
        self._root = None

    def size(self):
        return self._size(self._root)

    def _size(self, node):
        if not node:
            return 0

        cnt = 0
        if node.val:
            cnt += 1

        for i in range(256):
            cnt += self._size(node.next_nodes[i])

        return cnt

    def get(self, key):
        tmp = self._root
        d = 0

        while tmp:
            if d == len(key):
                return tmp.val
            char = key[d]
            tmp = tmp.next_nodes[ord(char)]
            d += 1
        return None

    def put(self, key, value):
        self._root = self._put(self._root, key, value, 0)

    def _put(self, node, key, value, d):
        if node is None:
            node = Node()

        if d == len(key):
            node.val = value
            return node

        char = key[d]
        index = ord(char)
        node.next_nodes[index] = self._put(node.next_nodes[index], key, value, d + 1)
        return node


if __name__ == '__main__':
    doctest.testmod()
