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

    '''
    >>> trie = Trie()
    >>> test_data = ['she', 'sells', 'sea', 'shells', 'by', 'the', 'sea', 'shore']
    >>> for index, d in enumerate(test_data):
    ...     trie.put(d, index)
    >>> trie.size()
    8
    >>> [trie.get(i).val for i in test_data]
    [0, 1, 6, 3, 4, 5, 6, 7]
    >>> [i for i in trie.keys()]
    ['by', 'sea', 'sells', 'she', 'shells', 'shore', 'the']
    >>> [i for i in trie.keys_with_prefix('sh')]
    ['she', 'shells', 'shore']
    >>> [i for i in trie.keys_that_match('.he')]
    ['she', 'the']
    >>> [i for i in trie.keys_that_match('s..')]
    ['sea', 'she']
    >>> trie.longest_prefix_of('shellsort')
    6
    '''

    def __init__(self):
        self._root = None
        self._size = 0

    def size(self):
        return self._size

    def get(self, key):
        tmp = self._root
        d = 0

        while tmp:
            if d == len(key):
                return tmp
            char = key[d]
            tmp = tmp.next_nodes[ord(char)]
            d += 1
        return tmp

    def put(self, key, value):
        self._root = self._put(self._root, key, value, 0)
        # d = 0
        # tmp = self._root
        # while d <= len(key):
        #     if not tmp:
        #         tmp = Node()
        #     if d == len(key):
        #         self._size += 1
        #         tmp.val = value
        #         break
        #     index = ord(key[d])
        #     tmp = tmp.next_nodes[index]
        #     d += 1

    def _put(self, node, key, value, d):
        if node is None:
            node = Node()

        if d == len(key):
            self._size += 1
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
        if prefix == '':
            self._collect(self._root, prefix, q)
        else:
            start_node = self.get(prefix)
            self._collect(start_node, prefix, q)
        return q

    def _collect(self, node, prefix, q):
        if not node:
            return

        if node.val is not None:
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
            if node.val is not None:
                q.enqueue(prefix)
            return

        char = pattern[length]
        for i in range(256):
            if char == '.' or char == chr(i):
                self._keys_collect(node.next_nodes[i], prefix + chr(i), pattern, q)

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


class TNode(object):

    def __init__(self):
        self._char = None
        self._left = None
        self._right = None
        self._mid = None
        self._val = None

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, new_char):
        return self._char

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, node):
        self._mid = node

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value


class TernarySearchTries(object):

    def __init__(self):
        self._root = None

    def get(self, key):
        tmp = self._root
        d = 0
        while tmp:
            char = key[0]
            if char < tmp.val:
                tmp = tmp.left
            elif char > tmp.val:
                tmp = tmp.right
            else:
                if d < len(key) - 1:
                    tmp = tmp.mid
                    d += 1
        return tmp.val if tmp else None

    def put(self, key, value):
        tmp = self._root
        d = 0
        while d < len(key):
            char = key[d]
            if not tmp:
                tmp = TNode()
                tmp.char = char
            if char < tmp.char:
                tmp = tmp.left
            elif char > tmp.char:
                tmp = tmp.right
            else:
                if d < len(key) - 1:
                    tmp = tmp.mid
                    d += 1

if __name__ == '__main__':
    doctest.testmod()
