#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from basic_data_struct import Queue


class Node(object):

    def __init__(self):
        self._val = None
        self.next_nodes = {}

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
    >>> trie.delete('she')
    >>> trie.size()
    7
    >>> trie.get('she').val
    '''

    def __init__(self):
        self._root = Node()
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
            tmp = tmp.next_nodes[char]
            d += 1
        return tmp

    def put(self, key, value):
        tmp = self._root
        for i in key:
            if i not in tmp.next_nodes:
                tmp.next_nodes[i] = Node()
            tmp = tmp.next_nodes[i]
        tmp.val = value
        self._size += 1

    def keys(self):
        '''
        Return all the keys in trie tree.
        '''
        return self.keys_with_prefix('')

    def keys_with_prefix(self, prefix):
        '''
        Return all the keys starts with the given prefix in the trie tree.
        '''
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
            if chr(i) in node.next_nodes:
                self._collect(node.next_nodes[chr(i)], prefix + chr(i), q)

    def keys_that_match(self, pattern):
        '''
        Return all the keys match the given pattern in the trie tree.
        '''
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
            if (char == '.' or char == chr(i)) and chr(i) in node.next_nodes:
                self._keys_collect(node.next_nodes[chr(i)], prefix + chr(i), pattern, q)

    def longest_prefix_of(self, s):
        '''
        Return the longest prefix's length of the given string which the prefix is in the trie tree.
        '''
        tmp = self._root
        length = d = 0

        while tmp:
            if tmp.val:
                length = d
            if d == len(s):
                return length
            char = s[d]
            if char not in tmp.next_nodes:
                break
            tmp = tmp.next_nodes[char]
            d += 1

        return length

    def delete(self, key):
        self._root = self._delete(self._root, key, 0)
        self._size -= 1

    def _delete(self, node, key, d):
        if not node:
            return None

        if d == len(key):
            node.val = None
        else:
            index = key[d]
            node.next_nodes[index] = self._delete(node.next_nodes[index], key, d + 1)

        if node.val:
            return node

        for i in range(256):
            if chr(i) in node.next_nodes:
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
