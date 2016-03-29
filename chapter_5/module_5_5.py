#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import sys


class Node(object):

    def __init__(self, char, freq, left, right):
        self._char = char
        self._freq = freq
        self._left = left
        self._right = right

    def is_leaf(self):
        return self._left is None and self._right is None

    def __cmp__(self, other):
        return self._freq - other._freq


class Huffman(object):

    @staticmethod
    def compress():
        pass

    @staticmethod
    def expand():
        pass


if __name__ == '__main__':
    doctest.testmod()
