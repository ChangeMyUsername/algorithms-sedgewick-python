#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from basic_data_struct import Queue

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

    def keys(self):
        return self.keys_with_prefix('')

    def keys_with_prefix(self, prefix):
        q = Queue()
        self._collect(self._root, prefix, q)
        return q

    def _collect(self, node, prefix, q):
        if not node:
            return

        if node.val:
            q.enqueue(prefix)

        for i in range(256):
            self._collect(node.next_nodes[i], prefix + chr(i), q)

    def keys_that_match(self, pattern):
        q = Queue()
        self._keys_collect(self._root, '', pattern, q)
        return q

    def _keys_collect(self, node, prefix, pattern, q):
        length = len(prefix)
        if not node:
            return

        if length == len(pattern):
            if node.val:
                q.enqueue(prefix)
            return

        char = pattern[length]
        for i in range(255):
            if char == '.' or char == chr(i):
                self._keys_collect(node.next_nodes[i], prefix + char, pattern, q)

    def longest_prefix_of(self, s):
        tmp = self._root
        length = d = 0

        while tmp:
            if tmp.val:
                length = d

            if d == len(s):
                return length

            char = s[d]
            tmp = tmp.next_nodes[ord(char)]
            d += 1

        return length

    def delete(self, key):
        self._root = self._delete(self._root, key, 0)

    def _delete(self, node, key, d):
        if not node:
            return None

        if d == len(key):
            node.val = None
        else:
            index = ord(key[d])
            node.next_nodes[index] = self._delete(node.next_nodes[index], key, d + 1)

        if node.val:
            return node

        for i in range(256):
            if node.next_nodes[i]:
                return node
        return None

if __name__ == '__main__':
    doctest.testmod()
